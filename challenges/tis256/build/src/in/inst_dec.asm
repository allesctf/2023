tpu X0 Y0
	## ${ADDR_INST_DEC}

	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# read reg
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_DEC}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, DOWN
	mov UP, NIL

	# write reg
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_DEC}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov ACC, RIGHT
	mov DOWN, ACC
	sub 1
	mov ACC, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	# send ack
	mov DOWN, RIGHT
	mov ${ADDR_INST_DEC}, RIGHT
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
