#!/usr/bin/env python3
"""Translate remaining help texts and names in shoot.c, tweaks.c, and other files."""
import re, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # === shoot.c help texts ===
    ('"Advanced bracketing (expo, flash, DOF). Press shutter once."', '"高级包围曝光(曝光,闪光,景深)。按一次快门。"'),
    ('"Choose the variables to bracket:"', '"选择包围变量:"'),
    ('"Number of bracketed shots. Can be computed automatically."', '"包围拍摄张数。可自动计算。"'),
    ('"Exposure difference between two frames."', '"两张照片之间的曝光差异。"'),
    ('"Bracketing sequence order / type. Zero is always first."', '"包围顺序/类型。零总是第一个。"'),
    ('"Delay before starting the exposure."', '"开始曝光前的延迟。"'),
    ('"Also use ISO as bracket variable. Range: 100 - max AutoISO."', '"同时用ISO作为包围变量。范围:100 - 最大自动ISO。"'),
    ('"Take pictures at fixed intervals (for timelapse)."', '"以固定间隔拍摄(用于延时摄影)。"'),
    ('"Duration between two shots."', '"两次拍摄之间的间隔。"'),
    ('"How to trigger the intervalometer start:"', '"如何触发间隔拍摄开始:"'),
    ('"Start the intervalometer after X seconds / minutes / hours."', '"X秒/分/时后开始间隔拍摄。"'),
    ('"Stop the intervalometer after taking X shots."', '"拍摄X张后停止间隔拍摄。"'),
    ('"For very long exposures (several minutes)."', '"用于超长曝光(数分钟)。"'),
    ('"Turn the screen on/off while taking bulb exposure."', '"B门曝光时开/关屏幕。"'),
    ('"Use the LCD face sensor as a simple remote (avoids shake)."', '"用LCD面部传感器作为简易遥控(避免震动)。"'),
    ('"Clap your hands or pop a balloon to take a picture."', '"拍手或戳气球来触发拍摄。"'),
    ('"Picture taken when sound level becomes X dB above average."', '"声音超过平均值X dB时拍摄。"'),
    ('"Take a picture when subject is moving or exposure changes."', '"主体移动或曝光变化时拍摄。"'),
    ('"Choose when the picture should be taken:"', '"选择拍摄时机:"'),
    ('"Higher values = less sensitive to motion."', '"值越高=对运动越不敏感。"'),

    # === shoot.c names ===
    ('"Handheld Debug"', '"手持调试"'),
    ('"ISO Selection"', '"ISO选择"'),
    ('"Min Movie AutoISO"', '"视频最小自动ISO"'),
    ('"Max Movie AutoISO"', '"视频最大自动ISO"'),

    # === tweaks.c remaining ===
    ('"Screen orientation, position fine-tuning..."', '"屏幕方向、位置微调..."'),
    ('"Workarounds for disabling Canon graphics elements."', '"禁用佳能图形元素的变通方法。"'),

    # === More help texts across files ===
    ('"Slowest shutter speed for ETTR (longest exposure time)."', '"ETTR最慢快门速度(最长曝光时间)。"'),
    ('"Exposure target for ETTR. Recommended: -0.5 or -1 EV."', '"ETTR曝光目标。推荐:-0.5或-1 EV。"'),
    ('"How many bright pixels are allowed above the target level."', '"允许多少亮像素超过目标电平。"'),
    ('"Choose what color channels are allowed to be clipped."', '"选择允许溢出的颜色通道。"'),
    ('"Hack to adjust slowest shutter from main dial."', '"从主拨盘调整最慢快门。"'),
    ('"Make status beeps (1 = OK, 2 = need more pictures, 3 = error)."', '"状态提示音(1=正常,2=需更多照片,3=错误)。"'),
    ('"For camera nerds."', '"给相机极客。"'),

    # === bitrate.c help texts ===
    ('"Change H.264 bitrate. Be careful, recording may stop!"', '"更改H.264码率。注意,录制可能停止!"'),
    ('"Firmware default / CBR (recommended) / VBR (very risky)"', '"固件默认/CBR(推荐)/VBR(高风险)"'),
    ('"1.0x = Canon default, 0.4x = 30minutes, 1.4x = fast card."', '"1.0x=佳能默认,0.4x=30分钟,1.4x=高速卡。"'),
    ('"Quality factor (-16 = best quality). Try not to use it!"', '"质量因子(-16=最佳质量)。尽量不用!"'),
    ('"A = average, B = instant bitrate, Q = instant QScale."', '"A=平均,B=瞬时码率,Q=瞬时QScale。"'),
    ('"ML will pause CPU-intensive graphics if buffer gets full."', '"缓冲区满时ML将暂停CPU密集型图形。"'),
    ('"You may get higher bitrates if you record sound separately."', '"独立录音可获得更高码率。"'),
    ('"Time indicator while recording."', '"录制时的时间指示器。"'),

    # === focus.c help texts ===
    ('"Takes a picture when the subject comes in focus. MF only."', '"主体合焦时拍摄。仅手动对焦。"'),
    ('"Focus with arrow keys. MENU while REC = save focus point."', '"用方向键对焦。录制时按MENU保存对焦点。"'),
    ('"You can focus with arrow keys or with the LCD sensor"', '"可用方向键或LCD传感器对焦"'),
    ('"[Q]: fix here rack end point. SET+L/R: start point."', '"[Q]:固定切换终点。SET+左/右:起点。"'),
    ('"Press SET for rack focus, or PLAY to also start recording."', '"按SET切换对焦,或按PLAY同时开始录制。"'),
    ('"Takes pictures at different focus points."', '"在不同对焦点拍摄多张照片。"'),
    ('"Run the focus stacking sequence."', '"运行焦点合成序列。"'),
    ('"Tip: press MENU to interrupt the stacking sequence."', '"提示:按MENU中断合成序列。"'),
    ('"On some lenses, this may be reversed."', '"某些镜头可能方向相反。"'),
    ('"Sets up stack focus to use the same range as rack focus."', '"设置焦点合成使用与焦点切换相同的范围。"'),
    ('"Tuning parameters and prefs for rack/stack/follow focus."', '"切换/合成/跟随对焦的调节参数。"'),
    ('"Step size for focus commands (same units as in EOS Utility)"', '"对焦命令步长(与EOS Utility相同单位)"'),
    ('"Delay between two successive focus commands."', '"两次对焦命令之间的延迟。"'),
    ('"Wait for \'focus done\' signal before sending next command."', '"等待\'对焦完成\'信号后再发送下一条命令。"'),
    ('"Focus direction for Left and Right keys."', '"左/右键的对焦方向。"'),
    ('"Focus direction for Up and Down keys."', '"上/下键的对焦方向。"'),
    ('"Number of seconds before starting focus operation."', '"对焦操作开始前的秒数。"'),
    ('"Display DOF above Focus distance, in LiveView."', '"在实时取景中对焦距离上方显示景深。"'),

    # === zebra.c help texts ===
    ('"Enable/disable ML overlay graphics (zebra, cropmarks...)"', '"启用/禁用ML叠加图形(斑马纹、裁切标记...)"'),
    ('"Zebra stripes: show overexposed or underexposed areas."', '"斑马纹:显示过曝或欠曝区域。"'),
    ('"Luma: red/blue. RGB: show color of the clipped channel(s)."', '"亮度:红/蓝。RGB:显示溢出通道颜色。"'),
    ('"Underexposure threshold."', '"欠曝阈值。"'),
    ('"Overexposure threshold."', '"过曝阈值。"'),
    ('"You can hide zebras when recording."', '"录制时可隐藏斑马纹。"'),
    ('"Use RAW zebras if possible."', '"尽可能使用RAW斑马纹。"'),
    ('"RAW zebra underexposure threshold"', '"RAW斑马纹欠曝阈值"'),
    ('"(in EVs above the noise floor)"', "(高于噪点下限的EV值)"),
    ('"Show which parts of the image are in focus."', '"显示图像中合焦的区域。"'),
    ('"How to display peaking. Alpha looks nicer, but image lags."', '"峰值显示方式。Alpha更好看但有延迟。"'),
    ('"How many pixels are considered in focus (percentage)."', '"多少比例的像素被视为合焦(百分比)。"'),
    ('"Focus peaking color (fixed or color coding)."', '"峰值对焦颜色(固定或颜色编码)。"'),
    ('"Display LiveView image in grayscale."', '"以灰度显示实时取景图像。"'),
    ('"Zoom box for checking focus. Can be used while recording."', '"用于检查对焦的缩放框。可在录制时使用。"'),
    ('"Trigger Magic Zoom by focus ring or half-shutter."', '"通过对焦环或半按快门触发魔法缩放。"'),
    ('"Size of zoom box (small / medium / large / full screen)."', '"缩放框大小(小/中/大/全屏)。"'),
    ('"Size of zoom box (small / medium / large)."', '"缩放框大小(小/中/大)。"'),
    ('"Position of zoom box (fixed or linked to focus box)."', '"缩放框位置(固定或关联对焦框)。"'),
    ('"1:1 displays recorded pixels, 2:1 displays them doubled."', '"1:1显示原始像素,2:1放大两倍显示。"'),
    ('"How to show focus confirmation (green bars / split screen)."', '"对焦确认显示方式(合焦绿条/裂像屏)。"'),
    ('"Overlay any image in LiveView. In PLAY mode, press LV btn."', '"在实时取景中叠加任意图像。回放模式按LV键。"'),
    ('"Update the overlay whenever you take a picture."', '"每次拍摄时更新叠加图像。"'),
    ('"Exposure aid: display brightness from a small spot."', '"曝光辅助:显示小区域亮度。"'),
    ('"Spotmeter position: center or linked to focus box."', '"点测光位置:中心或关联对焦框。"'),
    ('"False color palettes for exposure, banding, green screen..."', '"曝光、条带、绿屏的伪彩色调色板..."'),
    ('"Exposure aid: shows the distribution of brightness levels."', '"曝光辅助:显示亮度级别分布。"'),
    ('"Choose between YUV-based (JPG) or RAW-based histogram."', '"选择YUV(JPG)或RAW直方图。"'),
    ('"Linear or logarithmic histogram."', '"线性或对数直方图。"'),
    ('"Waveform size: Small / Large / FullScreen."', '"波形图大小:小/大/全屏。"'),
    ('"Electronic level indicator in 0.5 degree steps."', '"电子水平仪,0.5度步进。"'),
    ('"Show the frame rate of overlay loop (zebras, peaking...)"', '"显示叠加循环的帧率(斑马纹、峰值...)"'),

    # === movtweaks.c help texts ===
    ('"Recording key behavior."', '"录制键行为。"'),
    ('"Require a long press on the REC key to start/stop recording."', '"需要长按录制键开始/停止录制。"'),
    ('"Override movie time limit (in minutes)."', '"覆盖视频时间限制(分钟)。"'),
    ('"Gradually ramp exposure when exceeding the time limit."', '"超过时间限制时平滑过渡曝光。"'),
    ('"Ramping speed in EV stops per second."', '"过渡速度,每秒EV档数。"'),
    ('"Restart movie recording automatically when it stops."', '"录制停止时自动重新开始录制。"'),
    ('"Show REC/STBY notifications."', '"显示录制/待机通知。"'),
    ('"Force LiveView in movie mode."', '"在视频模式强制实时取景。"'),

    # === config.c help texts ===
    ('"[GLOBAL] If you hold the SET button pressed at camera startup:"', '"[全局] 如果开机时按住SET按钮:"'),
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