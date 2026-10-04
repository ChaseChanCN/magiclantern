#!/usr/bin/env python3
"""Translate module README.rst Summary and Description fields to Chinese."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# Module name -> (Chinese summary, Chinese description)
TRANSLATIONS = {
    "adv_int": ("高级间隔拍摄", "间隔拍摄的高级过渡和曝光控制\n\n从当前相机设置创建关键帧,并指定应用关键帧的帧号。\n你可以选择要在关键帧中设置的参数和要忽略的参数。\n模块在间隔拍摄运行时线性过渡选定参数的值。\n"),
    "arkanoid": ("打砖块游戏", "在相机上玩打砖块游戏。\n"),
    "autoexpo": ("自动曝光", "实时取景中的自动曝光控制。\n"),
    "bench": ("基准测试", "内存和性能基准测试工具。\n"),
    "bolt_rec": ("Bolt录制", "Bolt视频录制模块。\n"),
    "bulb_nd": ("B门ND计算", "计算ND滤镜强度和B门时间。\n"),
    "crop_rec": ("裁切录制", "以裁切模式录制RAW视频,获得更高分辨率。\n"),
    "deflick": ("去闪烁", "去除延时拍摄中的闪烁。\n"),
    "dot_tune": ("DotTune自动对焦微调", "使用DotTune方法自动校准自动对焦微调。\n无需手动调整,自动扫描对焦微调值。\n"),
    "dual_iso": ("双ISO", "交替ISO拍摄以扩展动态范围。\n录制时在两个ISO值之间交替,后期合成获得更高动态范围。\n"),
    "ettr": ("自动向右曝光", "拍摄RAW时自动向右曝光(ETTR)。\n自动调整曝光使高光尽可能亮但不溢出,最大化信噪比。\n"),
    "file_man": ("文件管理器", "在相机上浏览和管理文件。\n"),
    "img_name": ("图像文件命名", "自定义图像文件名和编号。\n"),
    "lua": ("Lua脚本", "在相机上运行Lua脚本。\n支持用Lua语言编写自定义脚本来自动化相机操作。\n"),
    "mlv_lite": ("RAW视频(精简版)", "录制RAW视频(MLV格式,无声音,基本元数据)。\n按实时取景键开始录制。\n"),
    "mlv_play": ("MLV播放器", "回放RAW视频(MLV格式)。\n"),
    "mlv_rec": ("RAW视频(MLV)", "录制RAW视频(MLV格式)。\n支持无损压缩、声音录制、多种预览模式。\n"),
    "mlv_snd": ("MLV录音", "为RAW视频录制声音。\n"),
    "silent": ("静音拍摄", "在实时取景中静音拍摄,不移动快门机构。\n支持多种模式:简单、连拍、最佳对焦、狭缝扫描等。\n"),
    "selftest": ("自测", "Magic Lantern自测模块。\n运行各种测试以验证固件功能正常。\n"),
    "pic_view": ("图片查看器", "在相机上查看图片。\n"),
    "script": ("脚本", "运行自定义脚本。\n"),
    "raw_twk": ("RAW调整", "调整RAW图像参数。\n"),
    "io_crypt": ("IO加密", "加密存储卡上的文件。\n"),
    "fpu_emu": ("浮点模拟", "软件浮点运算模拟。\n"),
    "tcc": ("TCC编译器", "内置TCC C编译器,可在相机上编译代码。\n"),
    "yolo": ("YOLO目标检测", "在实时取景中运行YOLO目标检测。\n"),
    "edmac": ("EDMAC查看器", "查看EDMA通道配置和状态。\n"),
    "edmaclog": ("EDMAC日志", "记录EDMA通道活动日志。\n"),
    "adtg_gui": ("ADTG调试", "查看和修改ADTG寄存器。\n"),
    "adtg_log": ("ADTG日志", "记录ADTG寄存器值日志。\n"),
    "iso_test": ("ISO测试", "测试各ISO值的噪声水平。\n"),
    "mem_chk": ("内存检查", "检查内存完整性。\n"),
    "mem_prot": ("内存保护", "内存访问保护测试。\n"),
    "mem_spy": ("内存监视", "监视内存访问。\n"),
    "devidlog": ("设备ID日志", "记录设备ID信息。\n"),
    "sf_dump": ("SF转储", "转储SF寄存器内容。\n"),
    "mrc_dump": ("MRC转储", "转储MRC寄存器内容。\n"),
    "mpu_dump": ("MPU转储", "转储MPU通信数据。\n"),
    "sd_clock": ("SD时钟调整", "调整SD卡时钟频率以超频。\n"),
    "plot": ("绘图", "在屏幕上绘制图形。\n"),
}

# Find all README.rst files
readmes = list((ROOT / "modules").rglob("README.rst"))
# Exclude build directories
readmes = [r for r in readmes if "build" not in str(r)]

total = 0
for rst_path in readmes:
    mod_dir = rst_path.parent
    mod_name = mod_dir.name
    
    if mod_name not in TRANSLATIONS:
        continue
    
    zh_summary, zh_desc = TRANSLATIONS[mod_name]
    
    try:
        content = rst_path.read_text(encoding="utf-8")
    except:
        continue
    
    orig = content
    
    # Replace the Summary line
    content = re.sub(
        r':Summary:\s*.*',
        f':Summary: {zh_summary}',
        content
    )
    
    # Replace the description (text between the metadata block and the first section)
    # The description is after the ":Forum:" line and before the first "----" section
    lines = content.split('\n')
    new_lines = []
    in_metadata = False
    past_metadata = False
    desc_replaced = False
    next_is_section = False
    
    for i, line in enumerate(lines):
        if line.startswith(':'):
            in_metadata = True
            new_lines.append(line)
            continue
        
        if in_metadata and line.strip() == '':
            in_metadata = False
            past_metadata = True
            new_lines.append(line)
            continue
        
        if past_metadata and not desc_replaced:
            # Check if this is a section header (like "Usage\n-----")
            if i + 1 < len(lines) and lines[i+1].startswith('---'):
                # This is a section title, stop replacing description
                new_lines.append(line)
                desc_replaced = True
                continue
            # Skip original description lines
            if line.strip() == '':
                continue
            # Check if next line is a section underline
            is_section = False
            if i + 1 < len(lines) and lines[i+1].startswith('---'):
                is_section = True
            
            if not is_section and not line.startswith('---'):
                # This is a description line, skip it
                continue
            else:
                # Insert Chinese description before the section
                if not desc_replaced:
                    new_lines.append(zh_desc)
                    new_lines.append('')
                    desc_replaced = True
                new_lines.append(line)
                continue
        
        new_lines.append(line)
    
    if not desc_replaced and past_metadata:
        # Insert Chinese description at the end of metadata
        insert_idx = 0
        for i, line in enumerate(new_lines):
            if line.startswith(':Forum:'):
                insert_idx = i + 1
                break
        if insert_idx > 0:
            new_lines.insert(insert_idx, '')
            new_lines.insert(insert_idx + 1, zh_desc)
    
    content = '\n'.join(new_lines)
    
    if content != orig:
        rst_path.write_text(content, encoding="utf-8")
        total += 1
        print(f"  Translated: {mod_name}")

print(f"\nTotal README files translated: {total}")