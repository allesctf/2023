tpu X0 Y0
	## ${ADDR_INST_JNZ}

	mov UP, DOWN
	mov UP, NIL
	mov UP, DOWN
	mov UP, NIL

	# get reg r0
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_JNZ}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov 0x00, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	jne 0, do_jmp
	mov DOWN, NIL
	jmp do_ack
do_jmp:

	# get rip
	mov ${ADDR_RIP}, RIGHT
	mov ${ADDR_INST_JNZ}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov 0x00, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# add offset
	add DOWN
	sub 16

	# request rip change
	mov ${ADDR_RIP}, RIGHT
	mov ${ADDR_INST_JNZ}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov 0x00, RIGHT
	mov ACC, RIGHT

	# receive response
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

do_ack:
	# send ack
	mov DOWN, RIGHT
	mov ${ADDR_INST_JNZ}, RIGHT
	mov ${OP_ACK}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT
end

tpu X1 Y0
	mov LEFT, UP
end

tpu X0 Y1
	mov UP, ACC
	mov UP, UP
	mov ACC, UP
end
