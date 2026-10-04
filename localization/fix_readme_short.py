#!/usr/bin/env python3
"""Fix the short description line (line 3) in module README.rst files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# Module name -> Chinese short description
SHORT_DESC = {
    "adv_int": "间隔拍摄的高级过渡和曝光控制",
    "arkanoid": "在相机上玩打砖块游戏",
    "autoexpo": "实时取景中的自动曝光控制",
    "bench": "内存和性能基准测试工具",
    "bolt_rec": "Bolt视频录制模块",
    "bulb_nd": "计算ND滤镜强度和B门时间",
    "crop_rec": "以裁切模式录制RAW视频,获得更高分辨率",
    "deflick": "去除延时拍摄中的闪烁",
    "dot_tune": "使用DotTune方法自动校准自动对焦微调",
    "dual_iso": "交替ISO拍摄以扩展动态范围",
    "ettr": "拍摄RAW时自动向右曝光(ETTR)",
    "file_man": "在相机上浏览和管理文件",
    "img_name": "自定义图像文件名和编号",
    "lua": "在相机上运行Lua脚本",
    "mlv_lite": "录制RAW视频(MLV格式,精简版)",
    "mlv_play": "回放RAW视频(MLV格式)",
    "mlv_rec": "录制RAW视频(MLV格式)",
    "mlv_snd": "为RAW视频录制声音",
    "silent": "在实时取景中静音拍摄,不移动快门机构",
    "selftest": "Magic Lantern自测模块",
    "pic_view": "在相机上查看图片",
    "script": "运行自定义脚本",
    "raw_twk": "调整RAW图像参数",
    "io_crypt": "加密存储卡上的文件",
    "fpu_emu": "软件浮点运算模拟",
    "tcc": "内置TCC C编译器",
    "yolo": "在实时取景中运行YOLO目标检测",
    "edmac": "查看EDMA通道配置和状态",
    "edmaclog": "记录EDMA通道活动日志",
    "adtg_gui": "查看和修改ADTG寄存器",
    "adtg_log": "记录ADTG寄存器值日志",
    "iso_test": "测试各ISO值的噪声水平",
    "mem_chk": "检查内存完整性",
    "mem_prot": "内存访问保护测试",
    "mem_spy": "监视内存访问",
    "devidlog": "记录设备ID信息",
    "sf_dump": "转储SF寄存器内容",
    "mrc_dump": "转储MRC寄存器内容",
    "mpu_dump": "转储MPU通信数据",
    "sd_clock": "调整SD卡时钟频率",
    "plot": "在屏幕上绘制图形",
}

readmes = list((ROOT / "modules").rglob("README.rst"))
readmes = [r for r in readmes if "build" not in str(r)]

total = 0
for rst_path in readmes:
    mod_name = rst_path.parent.name
    if mod_name not in SHORT_DESC:
        continue
    
    try:
        content = rst_path.read_text(encoding="utf-8")
    except:
        continue
    
    lines = content.split('\n')
    
    # Find the short description line (first non-empty line after title underline)
    # Line 0: title, Line 1: ===, Line 2: blank, Line 3: short desc
    if len(lines) > 3 and lines[1].startswith('==='):
        # Find the short description line
        for i in range(2, min(len(lines), 6)):
            if lines[i].strip() and not lines[i].startswith(':') and not lines[i].startswith('==='):
                # This is the short description line
                lines[i] = SHORT_DESC[mod_name]
                break
    
    new_content = '\n'.join(lines)
    if new_content != content:
        rst_path.write_text(new_content, encoding="utf-8")
        total += 1

print(f"Fixed short descriptions in {total} files")