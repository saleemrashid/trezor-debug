# trezor-debug

## Features

 * Intuitive read-write to memory-mapped registers
 * Tab completion
 * Integers displayed as hexadecimal

## Usage

```bash
$ make # Generate Python code from libopencm3 header files
$ ./main.py # Start REPL
(InteractiveConsole)
>>> RNG_DR
0x86d438d4
>>> FLASH_SR
0x80
>>> FLASH_SR |= FLASH_SR_PGSERR
>>> FLASH_SR
0x0
```

## Warnings

 * Since the firmware runs in unprivileged mode, privileged registers will
   cause a memory fault

 * Unlocking the flash (with `FLASH_KEYR`) will make the device unusable until
   the MCU is reset
