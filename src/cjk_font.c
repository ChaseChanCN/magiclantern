#include "dryos.h"
#include "bmp.h"
#include "cjk_font.h"

/*
 * CJK font overlay implementation.
 * Loads CRBF font files from ML/FONTS/ and provides glyph lookup + UTF-8 decode.
 */

/* safe unaligned little-endian reads (ARMv5 has no unaligned word load) */
static uint16_t rd16(const char *p) { uint16_t v; memcpy(&v, p, 2); return v; }
static uint32_t rd32(const char *p) { uint32_t v; memcpy(&v, p, 4); return v; }

#define CJK_NSIZES 4
static const int cjk_heights[CJK_NSIZES] = { 12, 23, 28, 32 };

typedef struct {
    uint32_t cp;
    uint16_t width;
    uint16_t advance;
    uint32_t off;
} cjk_glyph_t;

typedef struct {
    int height;
    int count;
    cjk_glyph_t *glyphs;   /* sorted by cp */
    char *data;            /* bitmap buffer */
    int data_size;
    int loaded;
} cjk_size_t;

static cjk_size_t cjk_sizes[CJK_NSIZES];

/* pick the closest available size slot for a requested height */
static int cjk_pick_size(int height)
{
    int best = 0;
    int best_diff = 1 << 30;
    for (int i = 0; i < CJK_NSIZES; i++)
    {
        if (!cjk_sizes[i].loaded) continue;
        int d = cjk_sizes[i].height - height;
        if (d < 0) d = -d;
        if (d < best_diff) { best_diff = d; best = i; }
    }
    return best;
}

static int cjk_load_one(const char *filename, cjk_size_t *cs)
{
    uint32_t fsize = 0;
    int r = FIO_GetFileSize(filename, &fsize);
    printf("[CJK] GetFileSize('%s')=%d size=%d\n", filename, r, fsize);
    if (r != 0 || fsize == 0)
        return 0;

    FILE *fd = FIO_OpenFile(filename, O_RDONLY | O_SYNC);
    printf("[CJK] OpenFile('%s')=%p\n", filename, fd);
    if (!fd) return 0;

    char *buf = malloc(fsize);
    printf("[CJK] malloc(%d)=%p\n", fsize, buf);
    if (!buf) { FIO_CloseFile(fd); return 0; }

    /* read in chunks <= 8192 to satisfy FIO_ReadFile's cacheable-buffer assert */
    uint32_t remaining = fsize;
    char *p = buf;
    while (remaining > 0)
    {
        uint32_t chunk = remaining > 8192 ? 8192 : remaining;
        int got = FIO_ReadFile(fd, p, chunk);
        if (got != (int)chunk) { free(buf); FIO_CloseFile(fd); return 0; }
        p += chunk;
        remaining -= chunk;
    }
    FIO_CloseFile(fd);

    if (fsize < 18 || buf[0] != 'C' || buf[1] != 'R' || buf[2] != 'B' || buf[3] != 'F')
    { free(buf); return 0; }

    /* header: magic(4) version(4) height(2) count(4) = 14 bytes */
    uint32_t version = rd32(buf + 4);
    (void)version;
    uint16_t height = rd16(buf + 8);
    uint32_t count  = rd32(buf + 10);
    if (count == 0 || count > 20000) { free(buf); return 0; }

    cs->glyphs = malloc(count * sizeof(cjk_glyph_t));
    if (!cs->glyphs) { free(buf); return 0; }

    /* parse records starting at offset 14; bitmap data goes into a separate buffer */
    /* First pass: compute total bitmap size */
    uint32_t off = 14;
    uint32_t total_bmp = 0;
    for (uint32_t i = 0; i < count; i++)
    {
        if (off + 8 > fsize) { free(buf); free(cs->glyphs); cs->glyphs = 0; return 0; }
        uint32_t cp     = rd32(buf + off);
        uint16_t width  = rd16(buf + off + 4);
        uint16_t adv    = rd16(buf + off + 6);
        int row_bytes = (width + 7) / 8;
        int bmp_size = row_bytes * height;
        cs->glyphs[i].cp = cp;
        cs->glyphs[i].width = width;
        cs->glyphs[i].advance = adv;
        cs->glyphs[i].off = total_bmp;
        total_bmp += bmp_size;
        off += 8 + bmp_size;
    }

    cs->data = malloc(total_bmp);
    if (!cs->data) { free(buf); free(cs->glyphs); cs->glyphs = 0; return 0; }
    cs->data_size = total_bmp;

    /* Second pass: copy bitmap bytes */
    off = 14;
    for (uint32_t i = 0; i < count; i++)
    {
        uint16_t width = rd16(buf + off + 4);
        int row_bytes = (width + 7) / 8;
        int bmp_size = row_bytes * height;
        memcpy(cs->data + cs->glyphs[i].off, buf + off + 8, bmp_size);
        off += 8 + bmp_size;
    }

    cs->height = height;
    cs->count = count;
    cs->loaded = 1;
    free(buf);
    return count;
}

int cjk_fonts_init(void)
{
    static int inited = 0;
    if (inited) return 0;
    inited = 1;

    int total = 0;
    static const char *names[CJK_NSIZES] = {
        "ML/fonts/cjk12.rbf",
        "ML/fonts/cjk23.rbf",
        "ML/fonts/cjk28.rbf",
        "ML/fonts/cjk32.rbf",
    };

    for (int i = 0; i < CJK_NSIZES; i++)
    {
        cjk_sizes[i].height = cjk_heights[i];
        int n = cjk_load_one(names[i], &cjk_sizes[i]);
        total += n;
        printf("[CJK] %s: %d glyphs\n", names[i], n);
    }
    printf("[CJK] total %d glyphs loaded\n", total);
    return total;
}

uint32_t utf8_decode(const char *s, int *adv)
{
    uint8_t b0 = (uint8_t)s[0];
    if (b0 < 0x80) { *adv = 1; return b0; }

    int n;
    uint32_t cp;
    if ((b0 & 0xE0) == 0xC0)      { n = 2; cp = b0 & 0x1F; }
    else if ((b0 & 0xF0) == 0xE0) { n = 3; cp = b0 & 0x0F; }
    else if ((b0 & 0xF8) == 0xF0) { n = 4; cp = b0 & 0x07; }
    else                          { *adv = 1; return b0; }

    for (int i = 1; i < n; i++)
    {
        uint8_t bi = (uint8_t)s[i];
        if ((bi & 0xC0) != 0x80) { *adv = 1; return b0; }
        cp = (cp << 6) | (bi & 0x3F);
    }
    *adv = n;
    return cp;
}

static cjk_glyph_t *cjk_find(cjk_size_t *cs, uint32_t cp)
{
    int lo = 0, hi = cs->count - 1;
    while (lo <= hi)
    {
        int mid = (lo + hi) >> 1;
        if (cs->glyphs[mid].cp == cp) return &cs->glyphs[mid];
        if (cs->glyphs[mid].cp < cp) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}

int cjk_glyph(uint32_t cp, int height, const char **cdata, int *cellw, int *pixw, int *gh)
{
    int si = cjk_pick_size(height);
    cjk_size_t *cs = &cjk_sizes[si];
    if (!cs->loaded) return 0;
    cjk_glyph_t *g = cjk_find(cs, cp);
    if (!g) return 0;
    int cell = (g->width + 7) & ~7;   /* next multiple of 8: row stride * 8 */
    if (cell == 0) cell = 8;
    *cdata = cs->data + g->off;
    *cellw = cell;
    *pixw = g->width;
    *gh = cs->height;
    return g->advance;
}

int cjk_has(uint32_t cp, int height)
{
    int si = cjk_pick_size(height);
    if (!cjk_sizes[si].loaded) return 0;
    return cjk_find(&cjk_sizes[si], cp) != 0;
}