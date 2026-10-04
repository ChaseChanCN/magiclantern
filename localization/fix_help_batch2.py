#!/usr/bin/env python3
"""Translate remaining help texts in shoot.c and other files."""
from pathlib import Path
import glob

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # shoot.c help texts (batch 2)
    ('"Size of the area on which motion shall be detected."', '"检测运动的区域大小。"'),
    ('"Delay between the detected motion and the picture taken."', '"检测到运动与拍摄之间的延迟。"'),
    ('"You can toggle MLU w. DirectPrint or link it to self-timer."', '"可用直接打印键切换反光板锁定,或关联自拍。"'),
    ('"You can link MLU with self-timer (handy)."', '"可将反光板锁定关联自拍(方便)。"'),
    ('"Choose when mirror lock-up should be active:"', '"选择反光板锁定启用时机:"'),
    ('"At what shutter speeds you want to use handheld MLU."', '"使用手持反光板锁定的快门速度。"'),
    ('"Delay between mirror and shutter movement."', '"反光板与快门运动之间的延迟。"'),
    ('"Check whether the \'mirror up\' event is detected correctly."', '"检查\'反光板升起\'事件是否正确检测。"'),
    ('"Experimental SRAW/MRAW mode. You may get corrupted files."', '"实验性SRAW/MRAW模式。可能产生损坏文件。"'),
    ('"After you take a picture, press SET to add a voice tag."', '"拍摄后按SET添加语音标签。"'),
    ('"Flash exposure compensation, 3rd party flash in LiveView..."', '"闪光曝光补偿,实时取景中的副厂闪光灯..."'),
    ('"Flash exposure compensation, from -10EV to +3EV."', '"闪光曝光补偿,从-10EV到+3EV。"'),
    ('"Take odd pictures with flash, even pictures without flash."', '"奇数张用闪光,偶数张不用闪光。"'),
    ('"Autofocus, number of pics to take at once..."', '"自动对焦、一次拍摄张数..."'),
    ('"How many pictures to take at once (for each trigger event)."', '"每次触发事件一次拍摄多少张。"'),
    ('"For intervalometer, audio remote shot and motion detect."', '"用于间隔拍摄、声控遥控和运动检测。"'),
    ('"Post-processing scripts for bracketing and focus stacking."', '"包围曝光和焦点合成的后处理脚本。"'),
    ('"Scripts for sorting intervalometer sequences."', '"用于排序间隔拍摄序列的脚本。"'),
    ('"You can take virtual (fake) pictures just for testing."', '"可拍摄虚拟(假)照片用于测试。"'),
    ('"Disable x5 or x10, boost contrast/sharpness..."', '"禁用x5或x10,增强对比度/锐度..."'),
    ('"Disable the screen that lets you move the focus box before zooming"', '"禁用缩放前移动对焦框的屏幕"'),
    ('"Disable x5 zoom in LiveView."', '"禁用实时取景x5缩放。"'),
    ('"Disable x10 zoom in LiveView."', '"禁用实时取景x10缩放。"'),
    ('"Auto adjusts exposure, so you can focus manually wide open."', '"自动调整曝光,以便全开光圈手动对焦。"'),
    ('"Increase sharpness and contrast when you zoom in LiveView."', '"实时取景缩放时增强锐度和对比度。"'),
    ('"Enable zoom when you hold the shutter halfway pressed."', '"半按快门时启用缩放。"'),
    ('"Zoom when you turn the focus ring (only some Canon lenses)."', '"转动对焦环时缩放(仅部分佳能镜头)。"'),
    ('"Double-click top-right button in LV. Shortcuts or Zoom."', '"在LV中双击右上角按钮。快捷键或缩放。"'),
    ('"Use the old Zoom In button, as in 5D2. Double-click in LV."', '"使用旧版放大按钮,如5D2。在LV中双击。"'),
    ('"Adjust Kelvin white balance and GM/BA WBShift."', '"调整开尔文白平衡和G/M、B/A白平衡偏移。"'),

    # shoot.c names (batch 2)
    ('"Motion Detect"', '"运动检测"'),
    ('"Motion Trigger"', '"运动触发"'),
    ('"Detect area size"', '"检测区域大小"'),
    ('"Trigger delay"', '"触发延迟"'),
    ('"Handheld MLU"', '"手持反光板锁定"'),
    ('"MLU delay"', '"反光板锁定延迟"'),
    ('"sRAW/mRAW"', '"sRAW/mRAW"'),
    ('"Snap Simulation"', '"快门模拟"'),
    ('"LiveView zoom tweaks"', '"实时取景缩放调整"'),
    ('"Increase SharpContrast"', '"增强锐度对比度"'),
    ('"Zoom on HalfShutter"', '"半按快门缩放"'),
    ('"Zoom with Focus Ring"', '"对焦环缩放"'),
    ('"Zoom with old button"', '"旧按钮缩放"'),
    ('"WBShift G/M"', '"白平衡偏移 G/M"'),
    ('"WBShift B/A"', '"白平衡偏移 B/A"'),

    # picstyle.c help texts
    ('"Change picture style."', '"更改照片风格。"'),
    ('"Sharpness strength."', '"锐度强度。"'),
    ('"Sharpness fineness."', '"锐度精细度。"'),
    ('"Sharpness threshold."', '"锐度阈值。"'),
    ('"Force a picture style for recording."', '"录制时强制使用照片风格。"'),
    ('"Picture style for recording."', '"录制用照片风格。"'),

    # powersave.c help texts
    ('"Turn off display after a few seconds of inactivity."', '"几秒不操作后关闭显示。"'),
    ('"Use the LCD sensor for turning off the display."', '"用LCD传感器关闭显示。"'),
    ('"Use a shortcut key for turning off the display."', '"用快捷键关闭显示。"'),

    # lens.c help texts
    ('"Display lens info."', '"显示镜头信息。"'),
    ('"Display logging info."', '"显示日志信息。"'),
    ('"Choose units for focus distance."', '"选择对焦距离单位。"'),
    ('"Display lens name."', '"显示镜头名称。"'),
    ('"Display lens ID."', '"显示镜头ID。"'),
    ('"Display serial number."', '"显示序列号。"'),
    ('"Display lens firmware version."', '"显示镜头固件版本。"'),
    ('"Display picture quality."', '"显示画质。"'),
    ('"Display ALO/HTP."', '"显示ALO/HTP。"'),
    ('"Display temperature."', '"显示温度。"'),
    ('"Display MVI number."', '"显示MVI编号。"'),
    ('"Display free space."', '"显示剩余空间。"'),
    ('"Display IS status."', '"显示防抖状态。"'),
    ('"Display focus distance."', '"显示对焦距离。"'),
    ('"Display AF/MF mode."', '"显示AF/MF模式。"'),

    # movtweaks.c help texts
    ('"Recording key behavior."', '"录制键行为。"'),
    ('"Require a long press on the REC key to start/stop recording."', '"需要长按录制键开始/停止录制。"'),
    ('"Override movie time limit (in minutes)."', '"覆盖视频时间限制(分钟)。"'),
    ('"Gradually ramp exposure when exceeding the time limit."', '"超过时间限制时平滑过渡曝光。"'),
    ('"Ramping speed in EV stops per second."', '"过渡速度,每秒EV档数。"'),
    ('"Restart movie recording automatically when it stops."', '"录制停止时自动重新开始录制。"'),
    ('"Show REC/STBY notifications."', '"显示录制/待机通知。"'),
    ('"Force LiveView in movie mode."', '"在视频模式强制实时取景。"'),

    # debug.c help texts
    ('"Browse memory contents."', '"浏览内存内容。"'),
    ('"Dump a memory range to a file."', '"将内存范围转储到文件。"'),
    ('"Read a value from a memory address."', '"从内存地址读取值。"'),
    ('"Write a value to a memory address."', '"向内存地址写入值。"'),
    ('"Turn the LCD into a flashlight."', '"将LCD变成手电筒。"'),
    ('"Take a screenshot after 10 seconds."', '"10秒后截图。"'),
    ('"Take screenshots of all menus."', '"截取所有菜单的截图。"'),
    ('"Log property changes."', '"记录属性变更。"'),
    ('"Unmount the SD card."', '"卸载SD卡。"'),
    ('"Log TryPostEvent calls."', '"记录TryPostEvent调用。"'),
    ('"Show DryOS tasks."', '"显示DryOS任务。"'),
    ('"Print task list."', '"打印任务列表。"'),
    ('"Print CPU usage."', '"打印CPU使用率。"'),
    ('"Print GUI events."', '"打印GUI事件。"'),
    ('"Test GUI modes."', '"测试GUI模式。"'),
    ('"Print image buffers."', '"打印图像缓冲区。"'),
    ('"Show total shutter count."', '"显示总快门计数。"'),
    ('"Show shutter/mirror/shots count."', '"显示快门/反光板/拍摄计数。"'),
    ('"Show internal temperature."', '"显示内部温度。"'),
    ('"Display property values."', '"显示属性值。"'),

    # module.c help texts
    ('"Show loaded modules."', '"显示已加载模块。"'),
    ('"Show hidden modules."', '"显示隐藏模块。"'),
    ('"Load modules after a crash."', '"崩溃后加载模块。"'),
    ('"Show module debug info."', '"显示模块调试信息。"'),

    # menuindex.c help texts
    ('"Choose what to do when pressing FUNC / PLAY."', '"选择按FUNC / PLAY时的操作。"'),
    ('"Choose what to do when pressing Pict.Style / PLAY."', '"选择按照片风格 / PLAY时的操作。"'),
    ('"Choose what to do when pressing JUMP / PLAY."', '"选择按JUMP / PLAY时的操作。"'),
    ('"Choose what to do when pressing Av / PLAY."', '"选择按Av / PLAY时的操作。"'),
    ('"Choose what to do when pressing Q / PLAY."', '"选择按Q / PLAY时的操作。"'),
    ('"Choose what to do on joystick long-press."', '"选择摇杆长按时的操作。"'),
    ('"Choose what to do when pressing SET or main dial."', '"选择按SET或主拨盘时的操作。"'),
    ('"Choose what to do when pressing Zoom In."', '"选择按放大键时的操作。"'),
    ('"Choose what to do when pressing MENU."', '"选择按MENU时的操作。"'),
    ('"Configure key shortcuts."', '"配置按键快捷方式。"'),

    # fps-engio.c help texts
    ('"Optimize FPS timer for movie or audio."', '"为视频或音频优化FPS定时器。"'),
    ('"Show main clock value."', '"显示主时钟值。"'),
    ('"Rolling shutter correction."', '"果冻效应校正。"'),
    ('"Sync FPS timer with shutter speed."', '"FPS定时器与快门速度同步。"'),
    ('"Ramp duration in seconds."', '"过渡持续时间(秒)。"'),

    # hdr.c help texts
    ('"HDR video by alternating ISO."', '"交替ISO录制HDR视频。"'),
    ('"ISO for frame A."', '"A帧ISO。"'),
    ('"ISO for frame B."', '"B帧ISO。"'),
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