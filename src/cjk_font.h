#ifndef CJK_FONT_H
#define CJK_FONT_H

/*
 * CJK (Chinese) font overlay for Magic Lantern.
 *
 * The stock ML RBF font engine is 8-bit (256 glyphs) and iterates strings
 * byte-by-byte, so UTF-8 Chinese renders as garbage.  This module loads
 * compact "CRBF" bitmap font files (one per size) from ML/FONTS/ and acts
 * as an overlay: Latin/ASCII keeps using the normal RBF fonts, while CJK
 * codepoints (>= 0x4E00) are drawn from the CRBF data.
 *
 * CRBF file format (little-endian):
 *   magic   b"CRBF"
 *   version uint32
 *   height  uint16   glyph cell height in pixels
 *   count   uint32
 *   count x {
 *     codepoint uint32
 *     width     uint16   pixel width
 *     advance   uint16   horizontal advance
 *     bitmap    height * ((width + 7) / 8) bytes, MSB-first, row-major
 *   }
 */

#include <stdint.h>

/* Load CRBF fonts from ML/FONTS/.  Safe to call once (idempotent).
   Returns total number of glyphs loaded across all sizes. */
int cjk_fonts_init(void);

/* Decode one UTF-8 sequence at `s` (need not be NUL-terminated, but the
   byte after a lead byte is read).  Returns the codepoint and sets *adv to
   the number of bytes consumed.  Invalid/incomplete sequences return the
   raw lead byte with *adv = 1 (so callers fall back to Latin rendering). */
uint32_t utf8_decode(const char *s, int *adv);

/* Look up a CJK glyph for codepoint `cp` at cell `height` px.
   On success returns the advance width in pixels and fills:
     *cdata  -> bitmap bytes (MSB-first, row-major, stride = cellw/8)
     *cellw  -> cell width in pixels (a multiple of 8, the row stride*8)
     *pixw   -> actual glyph pixel width (<= cellw)
     *gh     -> glyph cell height in pixels (rows of bitmap data)
   Returns 0 if the glyph is not present (caller should draw a fallback box). */
int cjk_glyph(uint32_t cp, int height, const char **cdata, int *cellw, int *pixw, int *gh);

/* 1 if cp can be rendered at the nearest available size, else 0. */
int cjk_has(uint32_t cp, int height);

#endif