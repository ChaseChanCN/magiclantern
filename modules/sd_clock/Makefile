# define the module name - make sure name is max 8 characters
MODULE_NAME = sd_clock
MODULE_OBJS = $(BUILD_DIR)/sd_uhs.o $(BUILD_DIR)/sd_pll.o $(BUILD_DIR)/sd_dryos_autotune.o
TOP_DIR = ../..

# include modules environment
include $(TOP_DIR)/modules/Makefile
.DEFAULT_GOAL := $(BUILD_DIR)/module_complete
