PREFIX    ?= arm-none-eabi-
CPP       := $(PREFIX)cpp

CPPFLAGS  += -Ilibopencm3/include

.PHONY: all clean

all: generated.py

clean:
	rm -f generated.py

generated.py: includes.h macros.py
	$(CPP) $(CPPFLAGS) -dDI $< | ./macros.py > $@
