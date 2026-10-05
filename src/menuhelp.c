/** \file
 * Magic Lantern menu help
 */
/*
 * Copyright (C) 2011 Alex Dumitrache <broscutamaker@gmail.com>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the
 * Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor,
 * Boston, MA  02110-1301, USA.
 */

#include "dryos.h"
#include "version.h"
#include "bmp.h"
#include "gui.h"
#include "config.h"
#include "property.h"
#include "lens.h"
#include "font.h"
#include "menu.h"
#include "menuhelp.h"

extern int menu_help_active;
static int current_page = 1;
static int help_pages = 100; // dummy value, will be updated on the fly

void 
draw_beta_warning()
{
    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);

    bmp_printf(FONT_CANON, 242, 53, "Magic Lantern");

    bmp_printf(FONT_MED | FONT_ALIGN_CENTER, 360, 150, "这是用于测试的开发版本。");

    bmp_printf(FONT_MED | FONT_ALIGN_CENTER, 360, 200, "请在 www.magiclantern.fm 报告所有问题。");

    bmp_printf(FONT_MED | FONT_ALIGN_CENTER, 360, 250, "请谨慎用于正式拍摄工作。");

    bmp_printf(FONT_MED | FONT_ALIGN_CENTER, 360, 300, "尽情享受！");

    bmp_printf(FONT_MED | FONT_ALIGN_CENTER, 360, 350, "(按任意相机按钮进入ML设置)");

    big_bmp_printf(FONT_MED,  10,  410,
        "Magic Lantern version: %s\n"
        "Git commit: %s\n"
        "Built on %s by %s.",
        build_version,
        build_id,
        build_date,
        build_user);
}

void 
draw_404_page()
{
    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);

    bmp_printf(FONT_CANON, 10, 20, "404 未记录的功能");

    bmp_printf(FONT_MED, 10, 100, "该功能可能尚未编写文档。");
    bmp_printf(FONT_MED, 10, 120, "毕竟我们是程序员，不是技术文档作者。");

    bmp_printf(FONT_MED, 10, 180, "不过...你可以直接试试看它有什么效果。");

    bmp_printf(FONT_MED, 10, 240, "然后写一段简短的描述，");
    bmp_printf(FONT_MED, 10, 260, "我们会将它加入用户手册。");

    bmp_printf(FONT_MED, 10, 320, "谢谢！");

}

void 
draw_help_not_installed_page()
{
    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);

    bmp_printf(FONT_CANON, 10, 20, "帮助文件未找到");
    
    bmp_printf(FONT_MED, 10, 150, "找不到Magic Lantern帮助文件。              ");

    bmp_printf(FONT_MED, 10, 200, "请确保所有ML文件已安装到存储卡。        ");

    bmp_printf(FONT_MED, 10, 250, "请访问 http://wiki.magiclantern.fm/install 查看说明。 ");
}

static void draw_help_content(int page)
{
    bmp_fill(COLOR_BLACK, 0, 0, 720, 480);
    int y = 15;

    switch(page)
    {
        case 1:
            bmp_printf(FONT_MED, 10, y, "关于 Magic Lantern"); y += 35;
            bmp_printf(FONT_MED, 10, y, "Magic Lantern（魔灯）是为"); y += 25;
            bmp_printf(FONT_MED, 10, y, "佳能相机提供额外功能的"); y += 25;
            bmp_printf(FONT_MED, 10, y, "开源软件增强平台。"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "以GPL许可证发布，在佳能"); y += 25;
            bmp_printf(FONT_MED, 10, y, "官方固件之上独立运行，"); y += 25;
            bmp_printf(FONT_MED, 10, y, "不修改原厂固件。"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "主要功能："); y += 25;
            bmp_printf(FONT_MED, 10, y, "HDR拍摄/间隔拍摄/手动音频"); y += 25;
            bmp_printf(FONT_MED, 10, y, "斑马纹/峰值对焦/RAW视频"); y += 25;
            bmp_printf(FONT_MED, 10, y, "焦点合成/电子水平仪"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "网站：magiclantern.fm"); y += 25;
            bmp_printf(FONT_MED, 10, y, "中文汉化版由Chase Chan维护"); y += 25;
            break;

        case 10:
            bmp_printf(FONT_MED, 10, y, "音频菜单 (Audio)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "音频控制"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  监听音量：提示音和回放音量"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  麦克风增益：手动调节增益"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  风声滤波：降低风噪声"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  音频波形：实时显示波形"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "录音设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  H.264码率：调节编码码率"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  时间码：SMPTE时间码显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  录制自动重启：自动重新开始"); y += 25;
            break;

        case 20:
            bmp_printf(FONT_MED, 10, y, "曝光菜单 (Expo)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "曝光控制"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  白平衡：推荐开尔文白平衡"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  光圈/快门/ISO：M档调节"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  曝光补偿：精细调节曝光"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  ETTR：向右曝光技术"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "包围曝光"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  张数：2/3/5/7/9张"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  步长：0.5/1/2/3 EV"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  顺序：正常->欠曝->过曝"); y += 25;
            break;

        case 30:
            bmp_printf(FONT_MED, 10, y, "叠加显示菜单 (Overlay)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "叠加显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  斑马纹：高亮过曝/欠曝区域"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  假色：颜色映射亮度级别"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  直方图：实时亮度直方图"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  矢量示波器：色彩分布分析"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "构图辅助"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  网格线：三分法/黄金比例"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  裁切标记：安全框显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  电子水平仪：双轴水平指示"); y += 25;
            break;

        case 40:
            bmp_printf(FONT_MED, 10, y, "视频菜单 (Movie)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "视频设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  H.264码率：CBR/VBR可调"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  码率预设：选择预设配置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  时间码：SMPTE时间码显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  录制自动重启：自动重新开始"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "视频工具"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  平滑曝光过渡：录像时平滑"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦点切换：两焦点间过渡"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  裁切模式：3x/5x数字变焦"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  RAW视频：14bit RAW视频流"); y += 25;
            break;

        case 50:
            bmp_printf(FONT_MED, 10, y, "拍摄菜单 (Shoot)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "拍摄功能"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  HDR拍摄：包围曝光合成"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  间隔拍摄：延时摄影"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  运动检测：画面变化触发"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  静音拍摄：电子快门无声"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "高级拍摄"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦点合成：景深合成拍摄"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  多重曝光：多次曝光叠加"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  闪光灯控制：外接闪光灯"); y += 25;
            break;

        case 60:
            bmp_printf(FONT_MED, 10, y, "对焦菜单 (Focus)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "对焦辅助"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  峰值对焦：高亮合焦区域"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  放大对焦：5x/10x精确对焦"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦距显示：显示当前焦距"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  合焦绿条：合焦确认显示"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "对焦工具"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦点切换：两焦点间过渡"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦点合成：自动改变焦点"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  跟踪对焦：跟踪画面目标"); y += 25;
            break;

        case 70:
            bmp_printf(FONT_MED, 10, y, "显示菜单 (Display)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "显示设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  LV DIGIC峰值对焦"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  LV亮度/对比度/饱和度"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  LV显示增益：增强取景亮度"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "信息显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  自定义信息显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  全局信息显示"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  焦距显示：显示当前焦距"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  拍摄信息：详细拍摄参数"); y += 25;
            break;

        case 80:
            bmp_printf(FONT_MED, 10, y, "偏好设置 (Prefs)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "偏好设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  自动开启ML：启动时加载"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  菜单颜色：选择配色方案"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  提示音：ML操作提示音"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "存储设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  SD/CF卡偏好设置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  配置文件：保存/加载配置"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  脚本：运行Lua脚本"); y += 25;
            break;

        case 90:
            bmp_printf(FONT_MED, 10, y, "调试菜单 (Debug)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "调试工具"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  任务调度：管理DryOS任务"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  内存信息：查看内存使用"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  寄存器：DIGIC/ADTG寄存器"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "诊断"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  温度监控：各部件温度"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  电池信息：查看电池状态"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  崩溃日志：查看崩溃记录"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "注意：仅供高级用户使用"); y += 25;
            break;

        case 92:
            bmp_printf(FONT_MED, 10, y, "模块菜单 (Modules)"); y += 35;
            bmp_printf(FONT_MED, 10, y, "ML支持可加载模块扩展功能。"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "模块状态"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  已加载：模块已成功加载"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  已禁用：模块被禁用"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  加载失败：模块加载出错"); y += 25;
            y += 15;
            bmp_printf(FONT_MED, 10, y, "可用模块"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  file_man：文件管理器"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  lua：Lua脚本支持"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  mlv_rec：MLV视频录制"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  silent：静音拍摄"); y += 25;
            bmp_printf(FONT_MED, 10, y, "  ettr：向右曝光"); y += 25;
            break;

        default:
            bmp_printf(FONT_MED, 10, 20, "帮助页面不可用");
            bmp_printf(FONT_MED, 10, 60, "该页面的详细帮助内容尚未生成。");
            bmp_printf(FONT_MED, 10, 100, "请查看菜单底部的帮助文本。");
            bmp_printf(FONT_MED, 10, 140, "访问 magiclantern.fm 查看文档。");
            break;
    }
}

void menu_help_show_page(int page)
{
    menu_help_active = 1;

    if (page == 0) { draw_404_page(); return; }
    if (page == -1) { draw_help_not_installed_page(); return; }

    draw_help_content(page);
}

void menu_help_redraw()
{
    BMP_LOCK( menu_help_show_page(current_page); );
}

void menu_help_next_page()
{
    current_page = MOD(current_page, help_pages) + 1;
    menu_help_active = 1;
}

void menu_help_prev_page()
{
    current_page = MOD(current_page - 2, help_pages) + 1;
    menu_help_active = 1;
}

void menu_help_go_to_page(int page)
{
    current_page = page;
    menu_help_active = 1;
}

void str_make_lowercase(char* s)
{
    while (*s) { *s = tolower(*s); s++; }
}

void menu_help_go_to_label(void* label, int delta)
{
    int page = 0; // if help page won't be found, will show 404
    if (is_menu_selected("Help"))
        page = 1; // don't show the 404 page in Help menu :P
    
    int size = 0;

    if (label == NULL)
        DryosDebugMsg(0, 15, "label was NULL");
    else
        DryosDebugMsg(0, 15, "label: %s", label);

    char* buf = (void*)read_entire_file("ML/doc/menuidx.dat", &size);
    if (!buf || !size)
        page = -1; // show "help not found" warning
    
    // trim spaces
    char label_adj[100];
    label_adj[0] = '\0';
    if (label != NULL)
    {   // this snprintf() implementation is not safe with NULL pointers
        snprintf(label_adj, sizeof(label_adj), "%s", label);
    }
    int i = strlen(label_adj);
    while (i > 0 && label_adj[i - 1] == ' ')
    {
        label_adj[i - 1] = '\0';
        i--;
    }
    str_make_lowercase(label_adj);

    int prev = -1;
    for (i = 0; i < size; i++)
    {
        if (buf[i] == '\n')
        {
            buf[i] = 0;
            char* line_buf = &buf[prev+1];

            char* name = line_buf+4;
            str_make_lowercase(name);
            int pagenum = atoi(line_buf);

            if(streq(name, label_adj))
                page = pagenum;
            help_pages = MAX(help_pages, pagenum);

            prev = i;
        }
    }

    fio_free(buf);
    
    current_page = page;
    menu_help_active = 1;
}
