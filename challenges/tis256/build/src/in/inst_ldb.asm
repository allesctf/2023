tpu X0 Y0
	## ${ADDR_INST_LDB}

	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov UP, DOWN

	# read reg src
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_LDB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# read memory [src]
	sav
	shr 6
	add ${ADDR_MEMORY_BASE}
	mov ACC, RIGHT
	swp
	mov ${ADDR_INST_LDB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# write reg dst
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_LDB}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov DOWN, RIGHT
	mov ACC, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	# send ack
	mov DOWN, RIGHT
	mov ${ADDR_INST_LDB}, RIGHT
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
