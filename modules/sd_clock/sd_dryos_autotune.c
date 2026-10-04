// Some ROMs have code to automatically determine
// a higher speed for SD cards.
//
// First noticed on 200D.  It's not called!
// This cam defaults to 40MB/s, increasing to 60MB/s
// simply by calling the function.
//
// Given that D5 cams can do 90MB/s, I would guess 200D can go faster,
// so presumably this autotune function is limited, or perhaps
// deliberately cautious.

#include "sd_dryos_autotune.h"

#include "dryos.h"
#include "menu.h"
#include "config.h"
#include "module.h"

#include "patch.h"
static int is_patched = 0;

extern WEAK_FUNC(ret_void) void autotune_SD(void);

static struct patch mode_192[] =
{
// 200D has code to autotune SD speed, but there seems to be a bug.
// There's an array which holds an index for selecting speed,
// out of a set starting 192Mhz, then 156, 130, 111.
// They loop over the possible speeds, but they increment the index
// at the top of the loop - the first possible speed is skipped.
// Thus it will never select higher than 156Mhz.
//
// We patch this table so it selects from 192, 156, 111.
// (even pretty old cards can do 156, but we keep the slowest "fast"
// speed as a fallback).

// e0ea7eb8 - this stores 192MHz mode index; 9, but it's never used (looks like a bug)
// e0ea7ebc - this stores 156Mhz mode index; 8, which is checked first
// e0ea7ec0 - this stores 130Mhz mode index; 7, checked second

    {
        .addr = (uint8_t *)0xe0ea7ebc,
        .old_value = 0x8,
        .new_value = 0x9,
        .size = 4,
        .description = "Allow 192MHz SD speed (156)"
    },
    {
        .addr = (uint8_t *)0xe0ea7ec0,
        .old_value = 0x7,
        .new_value = 0x8,
        .size = 4,
        .description = "Allow 156MHz SD speed (130)"
    },
};

static void autotune_SD_task()
{
    extern int ml_started;
    while (!ml_started)
        msleep(100); // Don't run during early boot while OS is still configuring SD.
                     // That seems to cause hangs.
                     // This is running as a task so sleeping is fine.
    if (!is_patched)
    {
        apply_patches(mode_192, COUNT(mode_192));
        is_patched = 1;
    }
    extern void autotune_SD(void);
    autotune_SD();
}

// Wraps DryOS function for ML.
// Note this isn't "enable" - I'm not aware of a "disable"
// function.  Presumably the card remains autotuned until next
// restart, or should the card error, when it will probably
// fallback to a lesser speed (this is speculation).
//
// Toggling the menu off -> on, will redo the autotune,
// possibly useful if the card ever resets and you don't
// want to restart cam?
static void run_SD_autotune(void *priv_unused, int unused)
{
    extern void autotune_SD(void);
    is_autotune_enabled = !is_autotune_enabled;

    if (is_autotune_enabled)
    {
        task_create("sd_autotune", 0x1c, 0x600, &autotune_SD_task, NULL);
    }
}

static struct menu_entry autotune_SD_speed_menu[] = {
    {
        .name = "SD速度自动调优",
        .priv = &is_autotune_enabled,
        .select = run_SD_autotune,
        .max = 1,
        .help = "运行佳能SD自动调优。可基准测试检查改善",
    }
};

unsigned int autotune_SD_init()
{
    if (is_camera("200D", "1.0.1"))
    {
        // So far only seen on this cam.  The patches are cam and fw ver specific,
        // if we ever expand this the code around mode_192 struct needs to be more
        // generic.
        if (is_autotune_enabled)
            task_create("sd_autotune", 0x1c, 0x600, &autotune_SD_task, NULL);
    }
    else
    {
        return 0;
    }

    menu_add( "Prefs", autotune_SD_speed_menu, COUNT(autotune_SD_speed_menu));
    return 0;
}

