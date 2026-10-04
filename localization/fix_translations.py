#!/usr/bin/env python3
"""Fix remaining untranslated strings, unclear translations, and help text."""
import re, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Targeted replacements: (old_string, new_string)
# These are exact string replacements in source files
REPLACEMENTS = [
    # === Help system messages ===
    ('"Help files not found"', '"帮助文件未找到"'),
    ('"Magic Lantern help files could not be found.              "', '"找不到Magic Lantern帮助文件。              "'),
    ('"Make sure all ML files are installed to your card.        "', '"请确保所有ML文件已安装到存储卡。        "'),
    ('"See http://wiki.magiclantern.fm/install for instructions. "', '"请访问 http://wiki.magiclantern.fm/install 查看说明。 "'),
    ('"Could not load help page %s."', '"无法加载帮助页面 %s."'),

    # === Display menu: tweaks.c ===
    # LV DIGIC peaking
    ('.name = "LV DIGIC peaking"', '.name = "LV DIGIC峰值对焦"'),
    ('"Slightly sharper"', '"轻微锐化"'),
    ('"Edge image"', '"边缘图像"'),
    ('"Edge + chroma"', '"边缘+色彩"'),
    ('"Focus peaking via DIGIC. No CPU usage!"', '"DIGIC峰值对焦,不占用CPU!"'),

    # LV brightness/contrast/saturation
    ('.name = "LV brightness"', '.name = "LV亮度"'),
    ('.name = "LV contrast"', '.name = "LV对比度"'),
    ('.name = "LV saturation"', '.name = "LV饱和度"'),
    ('"For LiveView preview only. Does not affect recording."', '"仅用于实时取景预览,不影响录制。"'),
    ('"Very high"', '"很高"'),
    ('"Very low"', '"很低"'),
    ('"Grayscale"', '"灰度"'),
    ('"Boost on WB adjust"', '"调白平衡时增强"'),
    ('"Boost on WB: increase saturation when you are adjusting WB."', '"调白平衡时增强:调整白平衡时提高饱和度。"'),

    # LV display gain
    ('.name = "LV display gain"', '.name = "LV显示增益"'),
    ('"Makes LiveView usable in complete darkness (photo mode)."', '"在完全黑暗中使用实时取景(照片模式)。"'),
    ('"Tip: if it gets really dark, also enable FPS override."', '"提示:如果太暗,可同时启用FPS覆盖。"'),

    # Clear overlays
    ('"Clear bitmap overlays from LiveView display."', '"清除实时取景中的位图叠加。"'),
    ('"WhenIdle"', '"空闲时"'),

    # Defishing
    ('"Rectilinear"', '"直线投影"'),
    ('"Panini"', '"Panini投影"'),
    ('"Preview straightened images from fisheye lenses. LV+PLAY."', '"预览鱼眼镜头矫正后的图像。LV+PLAY。"'),
    ('"Projection used for defishing (Rectilinear or Panini)."', '"去鱼眼投影方式(直线或Panini)。"'),
    ('"Projection"', '"投影方式"'),

    # Anamorphic
    ('"Stretches LiveView image vertically, for anamorphic lenses."', '"垂直拉伸实时取景图像,用于变形宽屏镜头。"'),
    ('"Aspect ratio used for anamorphic preview correction."', '"变形宽屏预览校正的宽高比。"'),
    ('"Stretch Ratio"', '"拉伸比例"'),

    # Advanced settings
    ('"Screen orientation, position fine-tuning..."', '"屏幕方向,位置微调..."'),
    ('"Kill Canon GUI"', '"屏蔽佳能界面"'),
    ('"Idle/Menus"', '"空闲/菜单"'),
    ('"Idle/Menus+Keys"', '"空闲/菜单+按键"'),
    ('"Workarounds for disabling Canon graphics elements."', '"禁用佳能图形元素的变通方法。"'),

    # === Fix unclear translations ===
    # Focus Stacking should be 焦点合成 not 焦点堆叠
    ('"焦点堆叠"', '"焦点合成"'),
    ('"运行焦点堆叠"', '"运行焦点合成"'),
    # Rack Focus should be 焦点切换 not 移位对焦
    ('"移位对焦"', '"焦点切换"'),
    # Gradual Exposure should be 平滑曝光过渡
    ('"渐变曝光"', '"平滑曝光过渡"'),
    # Ramping speed should be 过渡速度
    ('"渐变速度"', '"过渡速度"'),
    # Movie Restart should be 录制自动重启
    ('"视频重启"', '"录制自动重启"'),
    # Luma Fast should be 亮度快速模式
    ('"亮度快速"', '"亮度快速模式"'),
    # Green Bars should be 合焦绿条
    ('"绿条"', '"合焦绿条"'),

    # === More choices that need translation ===
    ('"Normal"', '"正常"'),
    ('"High"', '"高"'),
    ('"Low"', '"低"'),
    ('"Auto"', '"自动"'),

    # === Shoot menu help texts ===
    ('"Number of shots in front of current focus point."', '"当前对焦点前方的拍摄张数。"'),
    ('"Number of shots behind current focus point."', '"当前对焦点后方的拍摄张数。"'),
    ('"Number of focus steps between two pictures."', '"两张照片之间的对焦步数。"'),
    ('"Seconds between stack segments to let flashes recycle."', '"堆叠段之间的秒数,供闪光灯回电。"'),

    # === Movie tweaks help texts ===
    ('"Leave unchanged"', '"保持不变"'),
    ('"Block during REC"', '"录制时阻止"'),
    ('"Hold during REC"', '"录制时保持"'),

    # === Audio help texts ===
    ('"Gain applied to both inputs in analog domain (preferred)."', '"模拟域增益,作用于两个输入(推荐)。"'),
    ('"Digital gain (not recommended, use only for headphones!)"', '"数字增益(不推荐,仅用于耳机!)"'),
    ('"Digital gain (LEFT). Any nonzero value reduces quality."', '"数字增益(左声道)。任何非零值都会降低质量。"'),
    ('"Digital gain (RIGHT). Any nonzero value reduces quality."', '"数字增益(右声道)。任何非零值都会降低质量。"'),
    ('"Automatic Gain Control - turn it off :)"', '"自动增益控制 - 建议关闭 :)"'),
    ('"Audio input: internal / external / both / balanced / auto."', '"音频输入:内置/外部/两者/平衡/自动。"'),
    ('"High pass filter for wind noise reduction."', '"高通滤波器,用于降低风噪。"'),
    ('"Needed for int. and some other mics, but lowers impedance."', '"内置麦克风和某些麦克风需要,但会降低阻抗。"'),
    ('"Monitoring via A-V jack. Disable if you use a SD display."', '"通过A-V接口监听。使用SD显示时请禁用。"'),
    ('"Output volume for audio monitoring (headphones only)."', '"音频监听输出音量(仅耳机)。"'),

    # === Config help texts ===
    ('"Config auto save, manual save, restore defaults..."', '"配置自动保存、手动保存、恢复默认..."'),
    ('"Choose a configuration preset."', '"选择配置预设。"'),
    ('"If enabled, ML settings are saved automatically at shutdown."', '"启用后,ML设置在关机时自动保存。"'),
    ('"Save ML settings to current preset directory."', '"将ML设置保存到当前预设目录。"'),
    ('"This restores ML default settings, by deleting all CFG files."', '"通过删除所有CFG文件恢复ML默认设置。"'),
]

files = glob.glob(str(ROOT / "src" / "*.c")) + glob.glob(str(ROOT / "modules" / "*" / "*.c"))

total = 0
for f in files:
    p = Path(f)
    try:
        txt = p.read_text(encoding="utf-8")
    except:
        continue
    orig = txt
    for old, new in REPLACEMENTS:
        if old in txt:
            count = txt.count(old)
            txt = txt.replace(old, new)
            total += count
    if txt != orig:
        p.write_text(txt, encoding="utf-8")

print(f"Total replacements: {total}")