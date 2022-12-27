.PHONY: all clean

CC = gcc
C_SOURCES = $(wildcard *.c)
UPX = upx

all: exe_test

exe_test: $(C_SOURCES)
	@$(CC) $< -o $@
	@echo "[OK] Compiled: $@"

packed_exe: static_exe
	@$(UPX) -o $@ $<
	@echo "[OK] Packed: $@"
	@rm -f $<

static_exe: $(C_SOURCES)
	@$(CC) --static $< -o $@
	@echo "[OK] Compiled (static): $@"


clean:
	@rm -f exe_test static_exe packed_exe
