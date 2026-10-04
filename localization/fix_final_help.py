#!/usr/bin/env python3
"""Final batch: translate remaining English help strings."""
from pathlib import Path
import glob

translations = {
    "Always ON: just the Canon mode, press shutter twice.\\n": "始终开启:仅佳能模式,按两次快门。\\n",
    "Always ON: when you take a pic, or continuously in LiveView\\n": "始终开启:拍照时或实时取景中持续显示\\n",
    "Amount of jello effect. Multiply \\": "果冻效应强度。乘以\\",
    "DNG is slow, but needs no extra post-processing.\\n": "DNG较慢,但无需额外后期处理。\\n",
    "Do not load ML if you start the camera with SET pressed (default)\\n": "按SET开机时不加载ML(默认)\\n",
    "EXP: reacts to exposure changes (large movements).\\n": "EXP:响应曝光变化(大幅移动)。\\n",
    "Expo bracket. M: changes shutter. Others: changes AEcomp.\\n": "曝光包围。M档:改变快门。其他:改变AE补偿。\\n",
    "For LiveView preview only. Does not affect recording.\\n": "仅用于实时取景预览。不影响录制。\\n",
    "Original: default range used by Canon in selected video mode.\\n": "原始:佳能在所选视频模式中使用的默认范围。\\n",
    "Percentage of overall brightness level.\\n": "整体亮度水平的百分比。\\n",
    "Pickbox: SET shows a list of choices, select and confirm.\\n": "选择框:SET显示选项列表,选择并确认。\\n",
    "Scan from top to bottom as picture is taken.\\n": "拍照时从上到下扫描。\\n",
    "Simple: only consider defocus blur, ignoring diffraction effects.\\n": "简单:仅考虑离焦模糊,忽略衍射效应。\\n",
    "Start image capture on half-shutter press (quick).\\n": "半按快门开始图像捕获(快速)。\\n",
    "Strong edges: looks for edges, works best in low light.\\n": "强边缘:检测边缘,低光环境下效果最佳。\\n",
    "Take a silent picture when you press the shutter halfway.\\n": "半按快门时拍摄静音照片。\\n",
    "Take darker images.\\n": "拍摄更暗的图像。\\n",
    "When you exit ML menu, or at camera startup.\\n": "退出ML菜单时,或相机启动时。\\n",
    "When you set \\": "设置\\",
    "H.264码率。1单位=10 mb/s。 0 = Off": "H.264码率。1单位=10 mb/s。 0 = 关闭",
    "Total memory allocated by ML. 按SET查看详细信息。": "ML分配的总内存。按SET查看详细信息。",
}

src_dir = Path("../src")
modules_dir = Path("../modules")

total = 0
for f in list(src_dir.rglob("*.c")) + list(modules_dir.rglob("*.c")):
    try:
        text = f.read_text(encoding="utf-8")
    except:
        continue
    orig = text
    for old, new in translations.items():
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            total += count
    if text != orig:
        f.write_text(text, encoding="utf-8")

print(f"Total replacements: {total}")