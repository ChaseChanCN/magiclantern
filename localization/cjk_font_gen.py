#!/usr/bin/env python3
"""
Chinese (CJK) bitmap font generator for Magic Lantern.

Renders a set of Chinese characters from a system TrueType font (e.g. simhei.ttf)
into a compact binary "CRBF" font file that the patched ML font engine loads as an
overlay for CJK codepoints (>= 0x4E00).  ASCII/Latin continues to use the normal
RBF fonts; only CJK glyphs are stored here.

CRBF format (all little-endian):
    magic   : 4 bytes  = b"CRBF"
    version : uint32    = 1
    height  : uint16    glyph cell height in pixels
    count   : uint32    number of glyphs
    repeated count times:
        codepoint : uint32   Unicode codepoint
        width     : uint16   glyph width in pixels
        advance   : uint16   horizontal advance (== width + 1px gap)
        bitmap    : height * ((width + 7) // 8) bytes, MSB-first, row-major

Usage:
    python cjk_font_gen.py --chars chars.txt --size 32 --out cjk32.crbf
    python cjk_font_gen.py --size 32 --out cjk32.crbf   # uses built-in set
"""
import argparse
import struct
import sys
from pathlib import Path

DEFAULT_FONT = r"C:\Windows\Fonts\simhei.ttf"

# A broad built-in character set covering common camera / photo UI terms.
# The script will also accept extra characters via --chars so the font can be
# regenerated after translation to cover every glyph actually used.
BUILTIN_CHARS = (
    "曝光补偿光圈快门感光度白平衡对焦焦距焦点点测光中心加权平均局部"
    "评价测光高光阴影色调饱和度对比度锐度降噪降噪强度色温"
    "录制视频音频音量麦克风增益滤波器波形频率方波正弦白噪声"
    "菜单设置选项启用禁用开关是否确定取消返回上下左右选择"
    "照片图像格式分辨率宽高比比例帧率码率比特率时间码"
    "实时取景放大峰值对焦辅助斑马纹假色直方图矢量示波器"
    "水平垂直倾斜网格线裁切安全框显示隐藏自动手动关闭开启"
    "电源电池温度剩余空间存储卡版本日期时间语言简体中文"
    "高级恢复默认值全部保存加载配置文件脚本模块信息帮助关于"
    "警告错误失败成功提示确认操作不可用未支持已启用已禁用"
    "拍摄模式连拍单张包围曝光合成多重曝光延时自拍遥控"
    "动态范围优化高光恢复暗部细节黑白单色滤镜效果风格"
    "防抖稳定器跟踪人脸识别眼睛检测自动对焦手动对焦区域"
    "扩展最大最小限制警告建议信息默认自定义预设用户"
    "删除复制移动重命名新建文件夹浏览查看编辑搜索排序"
    "亮度背光闪烁补偿偏移步长单位精度快速慢速正常"
    "红外遥控快门线释放锁定半按全按合焦失焦模糊清晰"
    "动画静音输出输入通道左右声道平衡监听测试播放停止"
    "暂停录制中剩余时间已用时长文件名前缀编号序列连续"
    "覆盖询问覆盖确认保存到卡从卡加载导出导入重置"
    "日历时区夏令时格式小时分钟秒毫秒微秒帧场奇偶"
    "红绿蓝青品黄黑白灰透明不透明强度阈值范围区间"
    "缩放平移旋转镜像翻转裁剪缩略图全屏窗口标题状态"
    "日志调试级别打印输出控制台串口端口地址寄存器"
    "内存缓存堆栈指针任务进程线程优先级堆栈大小标志"
    "固件升级降级 bootloader 引导加载模块符号表校验和签名"
    "源目标副本原始备份临时永久只读写追加权限所有者"
    "更新检查下载上传安装卸载完成进度百分比速率速度"
    "延迟抖动丢包重传超时重试次数限制最大最小平均值"
    "峰值瞬时累计总计剩余可用已用容量大小类型名称路径"
    "确认要继续吗将丢失数据无法撤销请先停止录制"
    "按任意键返回按设置键确认按方向键选择"
    "，。、：；！？「」『』（）【】《》—…·°±×÷℃℉"
    "０１２３４５６７８９"
)


def render_glyph(font_path, ch, pixel_height):
    """Render one character to a 1-bit bitmap. Returns (width, rows[list of bytes])."""
    from PIL import Image, ImageDraw, ImageFont

    # Render at 4x then downscale for cleaner edges.
    scale = 4
    h = pixel_height * scale
    fnt = ImageFont.truetype(font_path, h)
    # Render on a large canvas, find actual content, then center it
    bbox = fnt.getbbox(ch)
    w = max(1, bbox[2] - bbox[0])
    # Use a tall canvas to render, then crop and center
    canvas_h = h * 2
    img = Image.new("1", (w, canvas_h), 0)
    d = ImageDraw.Draw(img)
    d.text((-bbox[0], (canvas_h - h) // 2 - bbox[1]), ch, font=fnt, fill=1)
    # Find actual content bounds
    content_bbox = img.getbbox()
    if content_bbox:
        content_h = content_bbox[3] - content_bbox[1]
        # Create final image with content vertically centered in h
        final = Image.new("1", (w, h), 0)
        paste_y = (h - content_h) // 2
        crop = img.crop((0, content_bbox[1], w, content_bbox[3]))
        final.paste(crop, (0, paste_y))
        img = final
    else:
        img = Image.new("1", (w, h), 0)
    if pixel_height != h:
        img = img.resize((max(1, w // scale), pixel_height), Image.LANCZOS)
    w = img.width
    # pack rows to bytes, LSB-first (matches ML's font_draw_char)
    rows = []
    for y in range(pixel_height):
        byte = 0
        bits = 0
        row_bytes = []
        for x in range(w):
            if img.getpixel((x, y)):
                byte |= (1 << bits)
            bits += 1
            if bits == 8:
                row_bytes.append(byte)
                byte = 0
                bits = 0
        if bits:
            row_bytes.append(byte)
        rows.append(bytes(row_bytes))
    return w, rows


def build_font(chars, font_path, pixel_height):
    """Build CRBF binary for the given unique characters."""
    seen = set()
    out = bytearray()
    out += b"CRBF"
    out += struct.pack("<I", 1)            # version
    out += struct.pack("<H", pixel_height) # height
    # placeholder count, filled later
    count_pos = len(out)
    out += struct.pack("<I", 0)
    count = 0
    for ch in chars:
        cp = ord(ch)
        if cp in seen:
            continue
        seen.add(cp)
        if cp < 0x20:
            continue
        try:
            width, rows = render_glyph(font_path, ch, pixel_height)
        except Exception as e:
            print(f"skip {ch!r} U+{cp:04X}: {e}", file=sys.stderr)
            continue
        advance = width + 1
        out += struct.pack("<I", cp)
        out += struct.pack("<H", width)
        out += struct.pack("<H", advance)
        for r in rows:
            out += r
        count += 1
    struct.pack_into("<I", out, count_pos, count)
    return bytes(out), count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chars", help="text file with extra characters to include")
    ap.add_argument("--size", type=int, default=32, help="glyph cell height in pixels")
    ap.add_argument("--out", required=True, help="output .crbf file")
    ap.add_argument("--font", default=DEFAULT_FONT, help="source TTF/TTC path")
    args = ap.parse_args()

    chars = set(BUILTIN_CHARS)
    if args.chars:
        chars.update(Path(args.chars).read_text(encoding="utf-8"))
    # always include ASCII printable
    chars.update(chr(c) for c in range(0x20, 0x7F))

    data, count = build_font(sorted(chars), args.font, args.size)
    Path(args.out).write_bytes(data)
    print(f"wrote {args.out}: {count} glyphs, {len(data)} bytes, height={args.size}")


if __name__ == "__main__":
    main()