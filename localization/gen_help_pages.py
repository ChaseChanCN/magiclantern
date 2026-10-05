#!/usr/bin/env python3
"""Generate ML help page BMP files and menuidx.dat for the help system."""
import struct
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("..")
FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
WIDTH, HEIGHT = 720, 480

# ML palette indices
BLACK = 9
WHITE = 15
GRAY_DARK = 10
GRAY_MED = 12
GRAY_LIGHT = 14
RED = 1
GREEN = 2
YELLOW = 6
ORANGE = 7

# ML palette in RGB (for BMP header, ML may ignore this but header needs to be valid)
PALETTE_RGB = [
    (0, 0, 0),       # 0 transparent
    (255, 0, 0),     # 1 red
    (0, 204, 0),     # 2 green
    (0, 0, 255),     # 3 blue
    (0, 255, 255),   # 4 cyan
    (255, 0, 255),   # 5 magenta
    (255, 255, 0),   # 6 yellow
    (255, 144, 0),   # 7 orange
    (0, 0, 0),       # 8 transparent black
    (0, 0, 0),       # 9 black
    (28, 28, 28),    # 10 gray1
    (64, 64, 64),    # 11 gray2
    (127, 127, 127), # 12 gray3
    (170, 170, 170), # 13 gray4
    (212, 212, 212), # 14 gray5
    (255, 255, 255), # 15 white
]

def make_palette_bmp():
    """Create a PIL image with ML palette."""
    img = Image.new("P", (WIDTH, HEIGHT), BLACK)
    pal = []
    for r, g, b in PALETTE_RGB:
        pal.extend([r, g, b])
    while len(pal) < 768:
        pal.extend([0, 0, 0])
    img.putpalette(pal)
    return img

def render_text_page(title, lines, page_num):
    """Render a help page with title and text lines."""
    img = make_palette_bmp()
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, WIDTH, 40], fill=GRAY_DARK)
    
    # Title text
    try:
        font_title = ImageFont.truetype(FONT_PATH, 5 * 4)
        font_body = ImageFont.truetype(FONT_PATH, 3 * 4)
        font_small = ImageFont.truetype(FONT_PATH, 2 * 4)
    except:
        font_title = ImageFont.load_default()
        font_body = font_title
        font_small = font_title
    
    # Scale down for anti-aliasing
    scale = 4
    big = Image.new("P", (WIDTH * scale, HEIGHT * scale), BLACK)
    pal = []
    for r, g, b in PALETTE_RGB:
        pal.extend([r, g, b])
    while len(pal) < 768:
        pal.extend([0, 0, 0])
    big.putpalette(pal)
    big_draw = ImageDraw.Draw(big)
    
    f_title = ImageFont.truetype(FONT_PATH, 28 * scale // 4)
    f_body = ImageFont.truetype(FONT_PATH, 18 * scale // 4)
    f_small = ImageFont.truetype(FONT_PATH, 14 * scale // 4)
    
    # Draw title bar
    big_draw.rectangle([0, 0, WIDTH * scale, 50 * scale], fill=GRAY_DARK)
    big_draw.text((10 * scale, 10 * scale), title, font=f_title, fill=WHITE)
    
    # Draw body text
    y = 60 * scale
    max_w = (WIDTH - 20) * scale
    for line in lines:
        if not line:
            y += 10 * scale
            continue
        
        color = WHITE
        if line.startswith("## "):
            color = YELLOW
            line = line[3:]
        elif line.startswith("# "):
            color = ORANGE
            line = line[2:]
        elif line.startswith("* "):
            color = GRAY_LIGHT
            line = "  " + line[2:]
        
        # Word wrap
        chars = list(line)
        cur_line = ""
        for ch in chars:
            test = cur_line + ch
            bbox = f_body.getbbox(test)
            if bbox and (bbox[2] - bbox[0]) > max_w:
                big_draw.text((10 * scale, y), cur_line, font=f_body, fill=color)
                y += 22 * scale
                cur_line = ch
            else:
                cur_line = test
        if cur_line:
            big_draw.text((10 * scale, y), cur_line, font=f_body, fill=color)
        y += 22 * scale
        
        if y > (HEIGHT - 20) * scale:
            break
    
    # Footer
    big_draw.text((10 * scale, (HEIGHT - 15) * scale), 
                  f"Magic Lantern 中文汉化版 - 第 {page_num} 页", 
                  font=f_small, fill=GRAY_MED)
    
    # Downscale
    img = big.resize((WIDTH, HEIGHT), Image.LANCZOS)
    img = img.convert("P", palette=Image.Palette.ADAPTIVE)
    
    # Re-apply ML palette
    final = Image.new("P", (WIDTH, HEIGHT), BLACK)
    pal = []
    for r, g, b in PALETTE_RGB:
        pal.extend([r, g, b])
    while len(pal) < 768:
        pal.extend([0, 0, 0])
    final.putpalette(pal)
    
    # Map pixels: white-ish -> 15, black-ish -> 9, etc.
    gray = img.convert("L")
    pixels = gray.load()
    final_pixels = final.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            v = pixels[x, y]
            if v < 20:
                final_pixels[x, y] = BLACK
            elif v < 60:
                final_pixels[x, y] = GRAY_DARK
            elif v < 120:
                final_pixels[x, y] = GRAY_MED
            elif v < 180:
                final_pixels[x, y] = GRAY_LIGHT
            else:
                final_pixels[x, y] = WHITE
    
    return final

def save_bmp(img, path):
    """Save PIL image as 8-bit indexed BMP."""
    img.save(str(path), format="BMP")

# Help page content - Chinese translations
help_pages = {
    1: ("关于 Magic Lantern", [
        "Magic Lantern（魔灯）是一个为佳能相机提供额外功能的开源软件增强平台。",
        "",
        "它以 GPL 许可证发布，在佳能官方固件之上独立运行，",
        "不会替换或修改原厂固件。",
        "",
        "# 主要功能",
        "* HDR 拍摄与包围曝光",
        "* 间隔拍摄（延时摄影）",
        "* 手动音频控制",
        "* 斑马纹与假色显示",
        "* 峰值对焦辅助",
        "* RAW 视频录制",
        "* 焦点合成与焦点切换",
        "* 电子水平仪",
        "* 自定义信息显示",
        "",
        "# 官方网站",
        "* http://magiclantern.fm/",
        "",
        "本版本为中文汉化版，由 Chase Chan 维护。",
    ]),
    10: ("音频菜单 (Audio)", [
        "# 音频控制",
        "* 监听音量：ML提示音和WAV回放音量(1-5)",
        "* 麦克风增益：手动调节麦克风增益",
        "* 风声滤波：降低风噪声",
        "* 音频波形：实时显示音频波形",
        "",
        "# 录音设置",
        "* H.264码率：可调节视频编码码率",
        "* 时间码：SMPTE时间码显示与同步",
        "* 录制自动重启：录制停止后自动重新开始",
    ]),
    20: ("曝光菜单 (Expo)", [
        "# 曝光控制",
        "* 白平衡：高级白平衡控制，推荐使用开尔文白平衡",
        "* 光圈/快门/ISO：在M档中独立调节",
        "* 曝光补偿：精细调节曝光",
        "* ETTR：向右曝光技术，最大化动态范围",
        "",
        "# 包围曝光",
        "* 包围拍摄张数：2/3/5/7/9张",
        "* 包围步长：0.5/1/2/3 EV",
        "* 包围顺序：正常->欠曝->过曝 或 欠曝->正常->过曝",
    ]),
    30: ("叠加显示菜单 (Overlay)", [
        "# 叠加显示",
        "* 斑马纹：高亮显示过曝/欠曝区域",
        "* 假色：用颜色映射亮度级别",
        "* 直方图：实时亮度直方图",
        "* 矢量示波器：色彩分布分析",
        "",
        "# 构图辅助",
        "* 网格线：三分法/黄金比例/自定义网格",
        "* 裁切标记：安全框显示",
        "* 电子水平仪：双轴水平指示",
    ]),
    40: ("视频菜单 (Movie)", [
        "# 视频设置",
        "* H.264码率：可调节编码码率(CBR/VBR)",
        "* 码率预设：选择预设码率配置",
        "* 时间码：SMPTE时间码显示",
        "* 录制自动重启：录制停止后自动重新开始",
        "",
        "# 视频工具",
        "* 平滑曝光过渡：录像时平滑改变曝光",
        "* 焦点切换：在两个焦点之间平滑过渡",
        "* 裁切模式：3x/5x数字变焦",
        "* RAW视频：录制14bit RAW视频流",
    ]),
    50: ("拍摄菜单 (Shoot)", [
        "# 拍摄功能",
        "* HDR拍摄：自动包围曝光合成",
        "* 间隔拍摄：延时摄影，可配置间隔和张数",
        "* 运动检测：基于画面变化触发快门",
        "* 静音拍摄：电子快门无声拍摄",
        "",
        "# 高级拍摄",
        "* 焦点合成：自动改变焦点拍摄多张用于景深合成",
        "* 多重曝光：单张照片叠加多次曝光",
        "* 闪光灯控制：外接闪光灯高级控制",
    ]),
    60: ("对焦菜单 (Focus", [
        "# 对焦辅助",
        "* 峰值对焦：高亮显示合焦区域",
        "* 放大对焦：5x/10x放大显示用于精确对焦",
        "* 焦距显示：显示当前镜头焦距",
        "* 合焦绿条：显示合焦确认绿条",
        "",
        "# 对焦工具",
        "* 焦点切换：在两个焦点之间平滑过渡",
        "* 焦点合成：自动改变焦点拍摄多张照片",
        "* 跟踪对焦：跟踪画面中的目标",
    ]),
    70: ("显示菜单 (Display)", [
        "# 显示设置",
        "* LV DIGIC峰值对焦：使用DIGIC处理器的峰值对焦",
        "* LV亮度/对比度/饱和度：实时取景画面调节",
        "* LV显示增益：增强实时取景亮度",
        "",
        "# 信息显示",
        "* 自定义信息显示：在屏幕上显示自定义参数",
        "* 全局信息显示：在所有模式下显示信息",
        "* 焦距显示：显示当前焦距",
        "* 拍摄信息：显示详细拍摄参数",
    ]),
    80: ("偏好设置 (Prefs)", [
        "# 偏好设置",
        "* 自动开启ML：相机启动时自动加载ML",
        "* 菜单颜色：选择菜单配色方案",
        "* 提示音：ML操作提示音",
        "",
        "# 存储设置",
        "* SD/CF卡相关偏好设置",
        "* 配置文件：保存/加载ML配置",
        "* 脚本：运行Lua脚本",
    ]),
    90: ("调试菜单 (Debug)", [
        "# 调试工具",
        "* 任务调度：查看和管理DryOS任务",
        "* 内存信息：查看内存使用情况",
        "* 寄存器查看：查看DIGIC/ADTG寄存器",
        "",
        "# 诊断",
        "* 温度监控：监控相机各部件温度",
        "* 电池信息：查看电池状态",
        "* 崩溃日志：查看ML崩溃记录",
        "",
        "# 注意",
        "调试菜单中的选项仅供高级用户使用。",
        "不当使用可能导致相机不稳定。",
    ]),
    92: ("模块菜单 (Modules)", [
        "# 模块系统",
        "ML支持可加载模块来扩展功能。",
        "",
        "# 模块状态",
        "* 已加载：模块已成功加载并可用",
        "* 已禁用：模块被禁用，不会加载",
        "* 加载失败：模块加载出错",
        "",
        "# 可用模块",
        "* file_man：文件管理器",
        "* lua：Lua脚本支持",
        "* mlv_rec：MLV视频录制",
        "* silent：静音拍摄",
        "* ettr：向右曝光",
        "* adv_int：高级间隔拍摄",
    ]),
}

# Generate menuidx.dat
menuidx_entries = [
    (1, "About Magic Lantern"),
    (1, "Help"),
    (10, "Audio"),
    (10, "Audio Meters"),
    (10, "AGC"),
    (10, "Input Volume"),
    (10, "Output Volume"),
    (10, "Wind Filter"),
    (10, "Loopback Volume"),
    (10, "Mic Insertion"),
    (10, "Beep"),
    (10, "Rec Volume"),
    (10, "H.264 Bitrate"),
    (10, "Timecode"),
    (10, "Movie Restart"),
    (20, "Expo"),
    (20, "WhiteBalance"),
    (20, "White Balance"),
    (20, "Kelvin"),
    (20, "WBShift G/M"),
    (20, "Picture Style"),
    (20, "Expo Override"),
    (20, "ISO"),
    (20, "Aperture"),
    (20, "Shutter"),
    (20, "Expo Compensation"),
    (20, "Auto ETTR"),
    (20, "Bracketing"),
    (30, "Overlay"),
    (30, "Global Draw"),
    (30, "Zebras"),
    (30, "False Color"),
    (30, "Histogram"),
    (30, "Vectorscope"),
    (30, "Waveform"),
    (30, "Clear Overlays"),
    (30, "Grid"),
    (30, "Cropmarks"),
    (30, "Level Indicator"),
    (30, "Focus Peaking"),
    (40, "Movie"),
    (40, "Movie Restart"),
    (40, "Movie Logging"),
    (40, "Raw Video"),
    (40, "Crop Mode"),
    (40, "Gradual Exposure"),
    (40, "Rack Focus"),
    (40, "Movie Bitrate"),
    (40, "Timecode"),
    (50, "Shoot"),
    (50, "HDR"),
    (50, "Intervalometer"),
    (50, "Motion Detect"),
    (50, "Silent Picture"),
    (50, "Focus Stacking"),
    (50, "Multiple Exposures"),
    (50, "Bulb Timer"),
    (60, "Focus"),
    (60, "Focus Peaking"),
    (60, "Focus Zoom"),
    (60, "Trap Focus"),
    (60, "Rack Focus"),
    (60, "Focus Stacking"),
    (60, "Follow Focus"),
    (70, "Display"),
    (70, "LV DIGIC Peaking"),
    (70, "LV Brightness"),
    (70, "LV Contrast"),
    (70, "LV Saturation"),
    (70, "LV Display Gain"),
    (70, "Global Draw"),
    (70, "Clear Screen"),
    (70, "Force HDMI/VGA"),
    (80, "Prefs"),
    (80, "Auto Boot"),
    (80, "Menu Color"),
    (80, "Beep"),
    (80, "Config File"),
    (80, "Scripts"),
    (80, "Preset"),
    (80, "Debug"),
    (90, "Debug"),
    (90, "Task Scheduler"),
    (90, "Memory Usage"),
    (90, "Prop Dump"),
    (90, "Register Dump"),
    (90, "Temperature"),
    (90, "Battery Info"),
    (90, "Crash Log"),
    (92, "Modules"),
    (92, "Module Load"),
    (92, "Module Info"),
]

# Generate BMP files
doc_dir = ROOT / "data" / "fonts" / "doc"
doc_dir.mkdir(parents=True, exist_ok=True)

for page_num, (title, lines) in help_pages.items():
    img = render_text_page(title, lines, page_num)
    bmp_path = doc_dir / f"page-{page_num:03d}.bmp"
    save_bmp(img, bmp_path)
    print(f"Generated page-{page_num:03d}.bmp")

# Generate menuidx.dat
dat_path = doc_dir / "menuidx.dat"
with open(dat_path, "w", encoding="utf-8") as f:
    for page, name in menuidx_entries:
        f.write(f"{page:03d} {name}\n")
print(f"Generated menuidx.dat with {len(menuidx_entries)} entries")

# Copy to build output
build_doc = ROOT / "platform" / "70D.112" / "build" / "zip" / "ML" / "doc"
build_doc.mkdir(parents=True, exist_ok=True)

import shutil
for f in doc_dir.iterdir():
    shutil.copy2(f, build_doc / f.name)
print(f"Copied {len(list(doc_dir.iterdir()))} files to build/zip/ML/doc/")