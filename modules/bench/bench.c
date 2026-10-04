/* Benchmarks */

#include <module.h>
#include <dryos.h>
#include <bmp.h>
#include <menu.h>
#include <screenshot.h>
#include <console.h>
#include <version.h>
#include <property.h>
#include <zebra.h>
#include <edmac-memcpy.h>
#include <powersave.h>
#include <shoot.h>

#include "cache.c"

extern void peaking_benchmark();
extern void menu_benchmark();

/* fixme: how to use multiple files without exporting a bunch of symbols from the module? */
#include "card_bench.c"
#include "mem_bench.c"
#include "mem_perf.c"

static struct menu_entry bench_menu[] =
{
    {
        .name        = "性能测试",
        .select        = menu_open_submenu,
        .help = "检查相机速度。卡、CPU、图形...",
        .submenu_width = 650,
        .children =  (struct menu_entry[]) {
            {
                .name        = "存储卡测试",
                .select        = menu_open_submenu,
                .help = "CF或SD卡基准测试",
                .children =  (struct menu_entry[]) {
                    {
                        .name = "Quick R/W benchmark (1 min)",
                        .select = run_in_separate_task,
                        .priv = card_benchmark_task_quick,
                        .help = "用16MB缓冲区检查卡读写速度。使用1GB临时文件。",
                        .help2 = "RAW视频建议在视频模式或回放模式运行。"
                    },
                    {
                        .name = "CF+SD写入测试(1分钟)",
                        .select = run_in_separate_task,
                        .priv = twocard_benchmark_task,
                        .help = "同时写入CF和SD卡的速度。",
                        .shidden = 1,   /* only appears if you have two cards inserted */
                    },
                    {
                        .name = "缓冲读写测试(5分钟)",
                        .select = run_in_separate_task,
                        .priv = card_benchmark_task_full,
                        .help = "检查各种缓冲区大小。RAW视频基准测试不需要,",
                        .help2 = "但如想优化视频缓冲算法,可尝试。"
                    },
                    {
                        .name = "缓冲写入测试(无限)",
                        .select = run_in_separate_task,
                        .priv = card_bufsize_benchmark_task,
                        .help = "寻找最佳写入缓冲区大小的实验。",
                        .help2 = "结果保存在BENCH.LOG。"
                    },
                    MENU_EOL,
                },
            },
            {
                .name        = "内存基准测试",
                .select        = menu_open_submenu,
                .help = "内存或缓存基准测试",
                .children =  (struct menu_entry[]) {
                    {
                        .name = "Memcpy benchmark (20s)",
                        .select = run_in_separate_task,
                        .priv = mem_benchmark_simple_task,
                        .help = "用不同子系统检查memcpy速度。",
                        .help2 = "(memcpy, dma_memcpy, DMA unit, EDMAC unit)"
                    },
                    {
                        .name = "Memory benchmark (1 min)",
                        .select = run_in_separate_task,
                        .priv = mem_benchmark_task,
                        .help = "用不同方法检查内存读写速度。",
                        .help2 = "(cacheable, uncacheable, EDMAC, different data types...)"
                    },
                    {
                        .name = "缓存测试(RAM)",
                        .select = run_in_separate_task,
                        .priv = mem_perf_test_cached,
                        .help = "通过基准测试检测RAM缓存大小(寻找速度骤降)。",
                        .help2 = "提示:加载'plot'模块获得好看的图表。",
                    },
                    {
                        .name = "缓存测试(RAM,无缓存)",
                        .select = run_in_separate_task,
                        .priv = mem_perf_test_uncached,
                        .help = "检查速度下降是否确实由缓存溢出引起。",
                        .help2 = "提示:加载'plot'模块获得好看的图表。",
                    },
                    {
                        .name = "缓存测试(ROM)",
                        .select = run_in_separate_task,
                        .priv = mem_perf_test_rom,
                        .help = "通过基准测试检测ROM缓存大小(寻找速度骤降)。",
                        .help2 = "提示:加载'plot'模块获得好看的图表。",
                    },
                    MENU_EOL,
                },
            },
            {
                .name        = "杂项基准测试",
                .select        = menu_open_submenu,
                .help = "峰值对焦和菜单后端基准测试(目前)",
                .children =  (struct menu_entry[]) {
                    {
                        .name = "Focus peaking benchmark (30s)",
                        .select = run_in_separate_task,
                        .priv = peaking_benchmark,
                        .help = "检查回放模式峰值对焦速度(1000次迭代)。",
                        .help2 = "卡上应有有效图像。"
                    },
                    {
                        .name = "Menu benchmark (10s)",
                        .select = run_in_separate_task,
                        .priv = menu_benchmark,
                        .help = "检查菜单后端速度。"
                    },
                    MENU_EOL,
                },
            },
            MENU_EOL,
        }
    },
};

/* fixme: only iterates the card benchmarks submenu */
static struct menu_entry * bench_menu_entry(const char* entry_name)
{
    /* menu entries are not yet linked, so iterate as in array, not as in linked list */
    for(struct menu_entry * entry = bench_menu[0].children[0].children ; !MENU_IS_EOL(entry) ; entry++ )
    {
        if (entry != NULL && entry->name != NULL && entry_name != NULL)
        {
            if (streq(entry->name, entry_name))
            {
                return entry;
            }
        }
    }
    return 0;
}

/* fixme: move to core */
static void bench_menu_show(const char* entry_name)
{
    struct menu_entry * entry = bench_menu_entry(entry_name);
    if (entry)
    {
        entry->shidden = 0;
    }
    else
    {
        console_show();
        printf("Could not find '%s'\n", entry_name);
    }
}


static void twocard_init()
{
    twocard_mq = (void*)msg_queue_create("twocard", 100);
    bench_menu_show("CF+SD write benchmark (1 min)");
}

static unsigned int bench_init()
{
    int cf_present = is_dir("A:/");
    int sd_present = is_dir("B:/");
    
    if (cf_present && sd_present)
    {
        twocard_init();
    }
    
    menu_add( "Debug", bench_menu, COUNT(bench_menu));
    
    return 0;
}

static unsigned int bench_deinit()
{
    return 0;
}

MODULE_INFO_START()
    MODULE_INIT(bench_init)
    MODULE_DEINIT(bench_deinit)
MODULE_INFO_END()
