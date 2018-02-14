#define STM32F2

/* These aren't available on the F2, but libopencm3 defines macros for them anyway */
#if defined(STM32F2)
#define GPIO_PORT_J_BASE 0x0
#define GPIO_PORT_K_BASE 0x0
#define SPI4_BASE 0x0
#define SPI5_BASE 0x0
#define SPI6_BASE 0x0
#endif

#include <libopencm3/cm3/mpu.h>
#include <libopencm3/stm32/desig.h>
#include <libopencm3/stm32/flash.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/memorymap.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/rng.h>
#include <libopencm3/stm32/spi.h>
