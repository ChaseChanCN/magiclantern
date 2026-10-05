#!/usr/bin/env python3
"""Generate menuidx.dat from ALL source files, mapping every menu item name."""
import re
from pathlib import Path

root = Path("../src")
modules = Path("../modules")

file_to_page = {
    "audio-ak.c": 10, "shoot.c": 50, "focus.c": 60, "tweaks.c": 70,
    "config.c": 80, "debug.c": 90, "zebra.c": 30, "histogram.c": 30,
    "falsecolor.c": 30, "vectorscope.c": 30, "lv-img-engio.c": 70,
    "movtweaks.c": 40, "bitrate-5d3.c": 40, "fps-engio.c": 40,
    "hdr.c": 50, "powersave.c": 80, "lens.c": 60, "picstyle.c": 20,
    "expo.c": 20, "ettr.c": 20, "bracket.c": 20, "selftest.c": 90,
    "menuindex.c": 80, "module.c": 92, "flexinfo.c": 70, "lvinfo.c": 70,
    "ph_info_disp.c": 70, "screenshot.c": 70, "crop-mode-hack.c": 40,
    "silent.c": 50, "motion_detect.c": 50, "intervalometer.c": 50,
    "io_crypt.c": 80, "edmac.c": 90, "mem.c": 90, "menuhelp.c": 1,
    "menu.c": 1, "gui.c": 1, "bmp.c": 70, "battery.c": 90,
    "bootflags.c": 80, "fileprefix.c": 80, "notify_box.c": 1,
    "dryos_rpc.c": 90, "property.c": 90, "propvalues.c": 90,
    "tasks.c": 90, "tskmon.c": 90, "init.c": 1, "raw.c": 50,
    "chdk-dng.c": 50, "chdk-gui_draw.c": 30, "compositor.c": 70,
    "greenscreen.c": 30, "imgconv.c": 70, "state-object.c": 90,
    "vram.c": 70, "vsync-lite.c": 90, "backtrace.c": 90, "log.c": 90,
    "patch.c": 90, "patch_mmu.c": 90, "patch_cache.c": 90,
    "patch_d6.c": 90, "mmu_utils.c": 90, "cpu.c": 90, "cache.c": 90,
    "cache_hacks.c": 90, "reloc.c": 90, "afma.c": 60,
    "af_patterns.c": 60, "dialog_test.c": 1, "electronic_level.c": 30,
    "exmem.c": 90, "fio-ml.c": 90, "font.c": 70, "imath.c": 90,
    "ico.c": 90, "rand.c": 90, "posix.c": 90, "stdio.c": 90,
    "util.c": 90, "version.c": 1, "console.c": 90, "tcc-glue.c": 90,
}

entries = []
seen_names = set()

top_menus = [
    (1, "Help"), (10, "Audio"), (20, "Expo"), (30, "Overlay"),
    (40, "Movie"), (50, "Shoot"), (60, "Focus"), (70, "Display"),
    (80, "Prefs"), (90, "Debug"), (92, "Modules"),
]
for page, name in top_menus:
    seen_names.add(name)
    entries.append((page, name))

for f in list(root.glob("*.c")) + list(modules.glob("*/*.c")):
    fname = f.name
    page = file_to_page.get(fname, 1)
    try:
        text = f.read_text(encoding="utf-8")
    except:
        continue
    for m in re.finditer(r'\.name\s*=\s*"([^"]+)"', text):
        name = m.group(1)
        if name not in seen_names and len(name) > 0:
            seen_names.add(name)
            entries.append((page, name))

entries.sort(key=lambda x: (x[0], x[1]))

dat_path = Path("../data/fonts/doc/menuidx.dat")
dat_path.parent.mkdir(parents=True, exist_ok=True)
with open(dat_path, "w", encoding="utf-8") as f:
    for page, name in entries:
        f.write(f"{page:03d} {name}\n")

print(f"Generated menuidx.dat with {len(entries)} entries")