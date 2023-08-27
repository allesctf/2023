PARTS = build/inst_jnz.asm build/inst_mov.asm build/inst_shl.asm build/inst_shr.asm \
	build/inst_inp.asm build/inst_out.asm build/test_in_out.asm build/gpr.asm

TEST_MOV_SWP = build/test_mov_swp.asm build/inst_mov.asm build/inst_swp.asm build/gpr.asm
TEST_SHL_SHR = build/test_shl_shr.asm build/inst_shl.asm build/inst_shr.asm build/gpr.asm
TEST_IN_OUT = build/test_in_out.asm build/inst_inp.asm build/inst_out.asm build/gpr.asm
TEST_ADD_SUB = build/test_add_sub.asm build/inst_add.asm build/inst_sub.asm build/gpr.asm

PARTS = build/inst_jnz.asm build/inst_shl.asm build/inst_shr.asm build/inst_mov.asm \
	build/inst_swp.asm build/inst_add.asm build/inst_sub.asm build/inst_xor.asm \
	build/inst_and.asm build/inst_ldb.asm build/inst_stb.asm build/inst_inp.asm \
	build/inst_out.asm build/inst_not.asm build/inst_jre.asm build/inst_inc.asm build/inst_dec.asm \
	build/cpu.asm build/rip.asm build/decoder.asm build/gpr.asm \
	build/memory1.asm build/memory2.asm build/memory3.asm build/memory4.asm

all: build/full_test_mov_swp.asm build/full_test_shl_shr.asm \
	build/full_test_in_out.asm build/full_test_add_sub.asm build/chall.asm

clean:
	rm -rf build

build:
	mkdir -p $@

build/memory1.bin build/memory2.bin build/memory3.bin build/memory4.bin: asm.py | build
	python3 asm.py $@

build/gpr.bin: in/gpr.bin | build
	cp $< $@

build/rip.bin: in/rip.bin | build
	cp $< $@

build/rip.asm.tmpl: memory.py build/rip.bin
	python3 memory.py $@ 0 0 build/rip.bin ADDR_RIP straight

build/gpr.asm.tmpl: memory.py build/gpr.bin
	python3 memory.py $@ 0 2 build/gpr.bin ADDR_GPR straight

build/memory1.asm.tmpl: memory.py build/memory1.bin
	python3 memory.py $@ 0 6 build/memory1.bin ADDR_MEMORY1 right

build/memory2.asm.tmpl: memory.py build/memory2.bin
	python3 memory.py $@ 64 6 build/memory2.bin ADDR_MEMORY2 left

build/memory3.asm.tmpl: memory.py build/memory3.bin
	python3 memory.py $@ 128 6 build/memory3.bin ADDR_MEMORY3 right

build/memory4.asm.tmpl: memory.py build/memory4.bin
	python3 memory.py $@ 192 6 build/memory4.bin ADDR_MEMORY4 left

build/%.asm: in/%.asm header.def | build
	tmpl -e -c header.def -p '$${' $< > $@

build/%.asm: build/%.asm.tmpl header.def | build
	tmpl -e -c header.def -p '$${' $< > $@

build/full_test_mov_swp.asm: bus.py $(TEST_MOV_SWP) | build
	python3 bus.py $@ $(TEST_MOV_SWP)

build/full_test_shl_shr.asm: bus.py $(TEST_SHL_SHR) | build
	python3 bus.py $@ $(TEST_SHL_SHR)

build/full_test_in_out.asm: bus.py $(TEST_IN_OUT) | build
	python3 bus.py $@ $(TEST_IN_OUT)

build/full_test_add_sub.asm: bus.py $(TEST_ADD_SUB) | build
	python3 bus.py $@ $(TEST_ADD_SUB)

build/full.asm: bus.py $(PARTS) | build
	python3 bus.py $@ \
	build/memory1.asm \
	build/cpu.asm build/inst_jnz.asm build/inst_mov.asm build/inst_shl.asm \
	build/rip.asm build/decoder.asm \
	build/inst_shr.asm build/inst_add.asm build/inst_sub.asm build/inst_xor.asm \
	build/memory2.asm \
	-- \
	build/memory3.asm \
	build/inst_and.asm build/inst_ldb.asm build/inst_stb.asm build/inst_inp.asm \
	build/gpr.asm build/inst_inc.asm \
	build/inst_out.asm build/inst_not.asm build/inst_jre.asm build/inst_swp.asm \
	build/memory4.asm

build/final.asm: draw.py build/full.asm misc/cat.png | build
	python3 draw.py build/full.asm misc/cat.png -86 -26 $@

build/chall.asm: transform.py build/final.asm | build
	python3 transform.py build/final.asm build/chall.asm

.PHONY: all clean
