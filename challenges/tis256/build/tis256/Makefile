PREFIX ?= /usr/local
BINDIR ?= /bin

CFLAGS = -Wunused-function -Wunused-variable -Wconversion -Wswitch
RAYLIB_SO ?= lib/raylib/build/raylib/libraylib.so
RAYLIB_SO_DIR = $(shell dirname "$(RAYLIB_SO)")

ifeq ($(DEBUG),1)
CFLAGS += -Og -g
else
CFLAGS += -O2
endif

all: tis256 tis256-curses tis256-gui tis256-vis

clean:
	rm -f tis256 tis256-curses tis256-gui tis256-vis

lib/raylib/.git:
	git submodule lib/raylib update --init --recursive

lib/raylib/build/raylib/libraylib.so: lib/raylib/.git
	cmake -S lib/raylib -B lib/raylib/build -D BUILD_SHARED_LIBS=1
	make -C lib/raylib/build

tis256: tis256.c tpu.c util.c asm.c tpu.h asm.h
	$(CC) -o $@ tis256.c tpu.c util.c asm.c $(CFLAGS)

tis256-curses: tis256-curses.c tpu.c util.c asm.c tpu.h asm.h
	$(CC) -o $@ tis256-curses.c tpu.c util.c asm.c $(CFLAGS) -lncursesw

tis256-gui: tis256-gui.c tpu.c util.c asm.c tpu.h asm.h
	$(CC) -o $@ tis256-gui.c tpu.c util.c asm.c $(CFLAGS) -lraylib

tis256-vis: tis256-vis.c util.c tpu.h asm.h $(RAYLIB_SO)
	$(CC) -o $@ tis256-vis.c util.c $(CFLAGS) -L "$(RAYLIB_SO_DIR)" -lraylib

install:
	install -m755 tis256 tis256-curses tis256-gui tis256-vis -t "$(DESTDIR)$(PREFIX)$(BINDIR)"

uninstall:
	rm -f "$(DESTDIR)$(PREFIX)$(BINDIR)"/{tis256,tis256-curses,tis256-gui,tis256-vis}

.PHONY: all clean install uninstall
