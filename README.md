# trezor-debug

## Features

 * Intuitive read-write to memory-mapped registers
 * Tab completion
 * Integers displayed as hexadecimal

## Usage

```bash
$ make # Generate Python code from libopencm3 header files
$ ./main.py # Start REPL
```

```python
(InteractiveConsole)
>>> RNG_DR # Read from memory-mapped registers
0x86d438d4
>>> FLASH_SR
0x80
>>> FLASH_SR |= FLASH_SR_PGSERR # Assign to memory-mapped registers
>>> FLASH_SR
0x0
>>> MMIO32(0x20015fcc).write(0xffffffff) # Writing to an arbitrary address
>>> MMIO32(0x20015fcc).read()
0xffffffff
>>> X = MMIO32(0x20015fcc) # Bind it to a variable to use normal assignment
>>> X = 0xffffffff
>>> X
0xffffffff
```

## Warnings

 * Since the firmware runs in unprivileged mode, privileged registers will
   cause a memory fault

 * Unlocking the flash (with `FLASH_KEYR`) will make the device unusable until
   the MCU is reset
