FILES = Makefile README ports.asm chall.asm asm.c asm.h tpu.c tpu.h util.c util.h \
		tis256.c tis256-gui.c tis256-curses.c

all: release/tis256.zip

clean:
	rm -rf release/tis256 release/tis256.zip
	rm -rf src/build

release:
	mkdir -p $@

release/tis256:
	mkdir -p $@

src/build/chall.asm: src/in/* src/*
	make -C src build/chall.asm

release/tis256/ports.asm: tis256/test/ports.asm | release/tis256
	cp $< $@

release/tis256/chall.asm: src/build/chall.asm | release/tis256
	cp $< $@

release/tis256/README: README | release/tis256
	cp $< $@

release/tis256/Makefile: release/Makefile | release/tis256
	cp $< $@

tis256/.git:
	git submodule tis256 update --init --recursive

release/tis256/%.c: tis256/%.c | release/tis256
	cp $< $@

release/tis256/%.h: tis256/%.h | release/tis256
	cp $< $@

release/tis256.zip: $(addprefix release/tis256/, $(FILES)) | release
	rm -f $@
	cd release && zip -r tis256.zip $(addprefix tis256/, $(FILES))

.PHONY: all clean
