#!/usr/bin/env python3
"""Translate remaining help texts in tweaks.c and other files."""
from pathlib import Path
import glob

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # tweaks.c help texts
    ('"Tweaks for LiveView focus box: move faster, snap to points."', '"实时取景对焦框调整:移动更快、吸附到预设点。"'),
    ('"Move the focus box faster (in LiveView)."', '"更快移动对焦框(实时取景中)。"'),
    ('"Snap the focus box to preset points (press CENTER key)"', '"对焦框吸附到预设点(按中心键)"'),
    ('"You can hide the focus box (the little white rectangle)."', '"可隐藏对焦框(白色小矩形)。"'),
    ('"Misc options related to shortcut keys."', '"快捷键相关杂项设置。"'),
    ('"Use the LCD face sensor as an extra key in ML."', '"将LCD面部传感器用作ML的额外按键。"'),
    ('"Makes the DOF preview button sticky (press to toggle)."', '"使景深预览按钮锁定(按一下切换)。"'),
    ('"Makes the half-shutter button sticky (press to toggle)."', '"使半按快门按钮锁定(按一下切换)。"'),
    ('"Swaps MENU and ERASE buttons."', '"交换MENU和ERASE按钮。"'),
    ('"Swaps INFO and PLAY buttons."', '"交换INFO和PLAY按钮。"'),
    ('"Show warning if some settings may cause problems."', '"某些设置可能导致问题时显示警告。"'),
    ('"Warn if the current mode is not optimal."', '"当前模式非最佳时警告。"'),
    ('"Warn if image quality is not optimal."', '"画质非最佳时警告。"'),
    ('"Warn if white balance is not optimal."', '"白平衡非最佳时警告。"'),
    ('"Custom warning message."', '"自定义警告消息。"'),
    ('"ISO/Kelvin"', '"ISO/开尔文"'),

    # tweaks.c choices
    ('"Arrow keys"', '"方向键"'),
    ('"LCD sensor"', '"LCD传感器"'),
    ('"Focus box"', '"对焦框"'),
    ('"Hide"', '"隐藏"'),
    ('"Show"', '"显示"'),

    # More help texts from various files
    ('"Choose what to do when you press FUNC / PLAY."', '"选择按FUNC / PLAY时的操作。"'),
    ('"Choose what to do when you press Pict.Style / PLAY."', '"选择按照片风格 / PLAY时的操作。"'),
    ('"Choose what to do when you press JUMP / PLAY."', '"选择按JUMP / PLAY时的操作。"'),
    ('"Choose what to do when you press Av / PLAY."', '"选择按Av / PLAY时的操作。"'),
    ('"Choose what to do when you press Q / PLAY."', '"选择按Q / PLAY时的操作。"'),
    ('"Choose what to do on joystick long-press."', '"选择摇杆长按时的操作。"'),
    ('"Choose what to do when you press SET or main dial."', '"选择按SET或主拨盘时的操作。"'),
    ('"Choose what to do when you press Zoom In."', '"选择按放大键时的操作。"'),
    ('"Choose what to do when you press MENU."', '"选择按MENU时的操作。"'),
    ('"Configure key shortcuts."', '"配置按键快捷方式。"'),

    # adv_int.c help texts
    ('"Advanced intervalometer with keyframes and ramping."', '"带关键帧和过渡的高级间隔拍摄。"'),
    ('"Use real time for keyframe timestamps."', '"关键帧时间戳使用真实时间。"'),
    ('"Loop the intervalometer after N shots."', '"拍摄N张后循环间隔拍摄。"'),
    ('"List all keyframes."', '"列出所有关键帧。"'),
    ('"Save keyframes to a file."', '"将关键帧保存到文件。"'),
    ('"Add a new keyframe."', '"添加新关键帧。"'),
    ('"Time of the current keyframe."', '"当前关键帧的时间。"'),
    ('"Time between two shots."', '"两次拍摄之间的时间。"'),

    # silent.c help texts
    ('"Take pics in LiveView without moving the shutter mechanism."', '"在实时取景中拍摄,不移动快门机构。"'),
    ('"Choose the silent picture mode:"', '"选择静音拍摄模式:"'),
    ('"Choose slitscan mode:"', '"选择狭缝扫描模式:"'),
    ('"Choose when to capture the image:"', '"选择图像捕获时机:"'),
    ('"File format to save the image as:"', '"图像保存格式:"'),

    # ettr.c help texts
    ('"Auto expose to the right when you shoot RAW."', '"拍摄RAW时自动向右曝光。"'),
    ('"When should the exposure be adjusted for ETTR:"', '"何时调整ETTR曝光:"'),
    ('"Slowest shutter speed for ETTR (longest exposure time)."', '"ETTR最慢快门(最长曝光时间)。"'),
    ('"Exposure target for ETTR. Recommended: -0.5 or -1 EV."', '"ETTR曝光目标。推荐:-0.5或-1 EV。"'),
    ('"How many bright pixels are allowed above the target level."', '"允许多少亮像素超过目标电平。"'),
    ('"Choose what color channels are allowed to be clipped."', '"选择允许溢出的颜色通道。"'),
    ('"Hack to adjust slowest shutter from main dial."', '"从主拨盘调整最慢快门。"'),
    ('"Make status beeps (1 = OK, 2 = need more pictures, 3 = error)."', '"状态提示音(1=正常,2=需更多照片,3=错误)。"'),
    ('"For camera nerds."', '"给相机极客。"'),

    # dot_tune.c help texts
    ('"Start the DotTune AFMA scan."', '"开始DotTune自动对焦微调扫描。"'),
    ('"Choose the scan type."', '"选择扫描类型。"'),
    ('"Number of scan passes."', '"扫描次数。"'),

    # bench.c help texts
    ('"Benchmark memory copy speed."', '"测试内存拷贝速度。"'),
    ('"Benchmark memory allocation speed."', '"测试内存分配速度。"'),
    ('"Benchmark focus peaking speed."', '"测试峰值对焦速度。"'),
    ('"Benchmark menu rendering speed."', '"测试菜单渲染速度。"'),

    # img_name.c help texts
    ('"Customize image file naming."', '"自定义图像文件命名。"'),
    ('"Custom image file prefix."', '"自定义图像文件前缀。"'),
    ('"Custom image file number."', '"自定义图像文件编号。"'),
    ('"Custom image folder number."', '"自定义图像文件夹编号。"'),

    # bulb_nd.c help texts
    ('"ND filter strength in stops."', '"ND滤镜强度(档数)。"'),
    ('"Measure ND filter strength."', '"测量ND滤镜强度。"'),

    # autoexpo.c help texts
    ('"Show exposure graph."', '"显示曝光图表。"'),
    ('"Use auto exposure in LiveView."', '"在实时取景中使用自动曝光。"'),
    ('"Lens aperture for auto exposure."', '"自动曝光的镜头光圈。"'),
    ('"Minimum shutter speed."', '"最慢快门速度。"'),
    ('"Use the same TV curve."', '"使用相同的TV曲线。"'),
    ('"ISO curve for auto exposure."', '"自动曝光的ISO曲线。"'),
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