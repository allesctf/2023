tpu X0 Y0
	## ${ADDR_DECODER}

	mov UP, DOWN
	mov UP, ACC
	mov UP, NIL
	mov UP, NIL
	sav

	and 0b11100000
	jeq 0, b5op
	swp
	sav

	and 0b11000000
	jeq 0b01000000, b2b3op
	swp
	sav

	and 0b11100000
	jeq 0b11100000, b2op
	swp
	sav

	jmp b2b2op

b5op:
	swp
	sav
	and 0b11100000
	mov ACC, RIGHT
	swp
	and 0b00011111
	mov ACC, RIGHT
	jmp wait

b2b3op:
	swp
	sav
	and 0b11100000
	mov ACC, RIGHT
	swp
	sav
	and 0b00011000
	shr 3
	mov ACC, RIGHT
	swp
	and 0b00000111
	mov ACC, RIGHT
	jmp wait

b2b2op:
	swp
	sav
	and 0b11110000
	mov ACC, RIGHT
	swp
	sav
	and 0b00001100
	shr 2
	mov ACC, RIGHT
	swp
	and 0b00000011
	mov ACC, RIGHT
	jmp wait

b2op:
	swp
	sav
	and 0b11111100
	mov ACC, RIGHT
	swp
	and 0b00000011
	mov ACC, RIGHT

wait:
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	mov DOWN, RIGHT
	mov ${ADDR_DECODER}, RIGHT
	mov ${OP_ACK}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT
end

tpu X0 Y1
	mov UP, UP
end

tpu X1 Y0
	mov LEFT, ACC

	jeq ${INST_JNZ}, inst_jnz
	jeq ${INST_SHL}, inst_shl
	jeq ${INST_SHR}, inst_shr
	jeq ${INST_MOV}, inst_mov
	jeq ${INST_SWP}, inst_swp
	jeq ${INST_ADD}, inst_add
	jeq ${INST_SUB}, inst_sub
	jeq ${INST_XOR}, inst_xor
	jeq ${INST_AND}, inst_and
	jeq ${INST_LDB}, inst_ldb
	jeq ${INST_STB}, inst_stb
	jeq ${INST_INP}, inst_inp
	jeq ${INST_OUT}, inst_out
	jeq ${INST_NOT}, inst_not
	jeq ${INST_JRE}, inst_jre
	jeq ${INST_INC}, inst_inc
	#jeq ${INST_DEC}, inst_dec
	${HLT}

inst_jnz:
	mov ${ADDR_INST_JNZ}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

inst_shl:
	mov ${ADDR_INST_SHL}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_shr:
	mov ${ADDR_INST_SHR}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_mov:
	mov ${ADDR_INST_MOV}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_swp:
	mov ${ADDR_INST_SWP}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_add:
	mov ${ADDR_INST_ADD}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_sub:
	mov ${ADDR_INST_SUB}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_xor:
	mov ${ADDR_INST_XOR}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_and:
	mov ${ADDR_INST_AND}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_ldb:
	mov ${ADDR_INST_LDB}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_stb:
	mov ${ADDR_INST_STB}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov LEFT, UP
	jmp wait

inst_inp:
	mov ${ADDR_INST_INP}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

inst_out:
	mov ${ADDR_INST_OUT}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

inst_not:
	mov ${ADDR_INST_NOT}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

inst_jre:
	mov ${ADDR_INST_JRE}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

inst_inc:
	mov ${ADDR_INST_INC}, UP
	mov ${ADDR_DECODER}, UP
	mov ${OP_NIL}, UP
	mov LEFT, UP
	mov ${OP_NIL}, UP
	jmp wait

#inst_dec:
#	mov ${ADDR_INST_DEC}, UP
#	mov ${ADDR_DECODER}, UP
#	mov ${OP_NIL}, UP
#	mov LEFT, UP
#	mov ${OP_NIL}, UP
#	jmp wait

wait:
	mov LEFT, UP
	mov LEFT, UP
	mov LEFT, UP
	mov LEFT, UP
	mov LEFT, UP
end
