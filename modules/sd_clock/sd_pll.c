#include "sd_pll.h"
#include "module.h"
#include "dryos.h"

// We don't know how to access SD UHS modes on Digic 4 cams,
// but it is possible to change what we believe is the PLL clock
// driving the card.
//
// This builds on previously known findings about a configurable
// timing unit.  See old wiki for more details:
// https://magiclantern.fandom.com/wiki/Register_Map
// ctrl-f for "Timer/Clock Module"

// 0xC0400004 [32]  Clock selection
//                    Bitmask
//                    0x03000000 SD/MMC clock selection bits
//                       0 unknown
//                       1 16MHz
//                       2 24MHz
//                       3 48MHz
//
// 0xC0400008 [32]  Clock control
//                    Bitmask - configures which module gets system clock
//                    0x00000002 Engio LCLK
//                    0x00000004 (ASIF related too)
//                    0x00000008 SD/MMC clock 1
//                    0x00000100 Display PWM module
//                    0x00000400 Timer #0
//                    0x00000800 Timer #1
//                    0x00001000 Timer #2
//                    0x00010000 LCLK (also set)
//                    0x00200000 SIO clock
//                    0x01000000 DMA module #0 (fIPCClk)
//                    0x01000000 IPC module on 7D
//                    0x02000000 ASIF
//                    0x10000000 SD/MMC clock 2

// The previously unknown c04000bc is used in this new code.
// That's combined with known ways to config "SD/MMC clock 2"
// to boost the clock.

#define CLOCK_SELECT_ADDR   0xc0400004
#define CLOCK_CONTROL_ADDR  0xc0400008
#define CLOCK_SD_PLL_ADDR   0xc04000bc // Is this SD related?  Or more general?
                                       // We can select different devices to set the clock for,
                                       // with CLOCK_CONTROL_ADDR.
#define CLOCK_SELECT_48MHz 0x03000000
#define CLOCK_DEVICE_SD 0x10000000 // "SD/MMC clock 2"
#define SD_PLL_STOCK 0x54fc8

static bool SD_initialised = false;

// The claim on these magic values is that some of the bits above 12th
// are used as a divisor to calc the SD freq.
// 
// Which bits are not confirmed.  Since we don't know how the higher clock
// speed that is being divided is derived, it's easy to fit different
// groups of bits with different theories.
//
// One theory - all the bits higher than 12:
// 0x54fc8 >> 0xc -> 0x54, subtract the fixed (3cfc8 >> 0xc) offset
// 0x54 - 0x3c -> 0x18 (24),
// 1152 / 24 = 48 Mhz
//
// Possibly simpler theory - 5c, 4c and 48 share their two low bits being 0,
// so assume these are fixed and not part of the divisor.
// Highest bit set is always set, so ignore from here upwards, too.
// That leaves, in bits f:c inclusive:
// 54 => 0101: 5
// 4c => 0011: 3
// 48 => 0010: 2
//
// If we *further* assume that 0 is an implicit divisor of 1,
// we get 6, 4, 3.  That would then fit like so:
// 288 / 6 = 48
// 288 / 4 = 72
// 288 / 3 = 96
// (288 / 2 = 144, but this doesn't work in practice, too fast?)
//
// Neither theory directly explains where the 1152 or 288 come from.
// Board photos for 600d, e.g. https://photo-parts.com.ua/parts/IMG_STORE/Canon%20600D%20files/600D%20main_1.jpg
// show a 54MHz crystal just next to the Digic 4 part.
// Strings in 600D and 1100D state a 132MHz system clock.
// wavesoft / Ioannis gives a plausible route: divide the xtal by 9 for 6MHz,
// which can then be multiplied up 22x for system clock, 4x for base SD clock.
//
// 5D3 1.2.3 initialises this to 0x54000, which fits both theories.
//
// The lower bits (fc8) may have some role in the SD clock, but evidence so far is limited.
static const uint32_t SD_PLL_values[] = {
    SD_PLL_STOCK, // 48 MHz, must be 1st item in this array, we assume index 0 is stock
    0x4cfc8, // 72 MHz
    0x48fc8, // 96 MHz
};

static MENU_UPDATE_FUNC(SD_PLL_update)
{
    if (!SD_initialised)
    {
        MENU_SET_WARNING(MENU_WARN_NOT_WORKING, "SD clock not init");
        return;
    }

    if (SD_PLL_clock_choice != 0)
        MENU_SET_WARNING(MENU_WARN_ADVICE, "Restart cam to apply change");
}

static struct menu_entry SD_PLL_menu[] = {
    {
        .name    = "SD频率",
        .priv    = &SD_PLL_clock_choice,
        .max     = COUNT(SD_PLL_values) - 1,
        .choices = CHOICES("48 MHz (stock)", "72 MHz", "96 MHz"),
        .update  = SD_PLL_update,
        .help    = "SD总线时钟。模块加载时应用;重启生效"
    },
};

// sets the PLL clock MMIO with appropriate magic value, from mode
static void set_SD_PLL_clock(uint32_t mode)
{
    if (mode >= COUNT(SD_PLL_values))
        return;

    uint32_t old_int = cli();
    // disable SD clock
    MEM(CLOCK_CONTROL_ADDR) &= ~CLOCK_DEVICE_SD;

    // adjust clock params
    MEM(CLOCK_SD_PLL_ADDR) = SD_PLL_values[mode];
    MEM(CLOCK_SELECT_ADDR) = MEM(CLOCK_SELECT_ADDR) | CLOCK_SELECT_48MHz;

    // enable SD clock
    MEM(CLOCK_CONTROL_ADDR) |= CLOCK_DEVICE_SD;
    sei(old_int);
}

// Attempt to apply whatever clock is selected in prefs menu
static void apply_selected_clock(void)
{
    if (!SD_initialised)
        return;

    if (SD_PLL_clock_choice < 0 || SD_PLL_clock_choice >= COUNT(SD_PLL_values))
        SD_PLL_clock_choice = 0;

    // 0 is index for stock 48MHz speed
    if (SD_PLL_clock_choice == 0)
        return;

    set_SD_PLL_clock(SD_PLL_clock_choice);

    // SJE TODO do filesystem data roundtrip tests here
}

unsigned int init_SD_PLL(void)
{
    // Only enable on tested cams.
    // Probably works on all D4 cams with SD slot.
    if (!is_camera("1100D", "*") && !is_camera("60D", "*"))
        return 0;

    SD_initialised = (MEM(CLOCK_SD_PLL_ADDR) == SD_PLL_STOCK);

    menu_add( "Prefs", SD_PLL_menu, COUNT(SD_PLL_menu));

    apply_selected_clock();
    return 0;
}
