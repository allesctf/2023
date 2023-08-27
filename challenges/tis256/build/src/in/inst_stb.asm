tpu X0 Y0
	## ${ADDR_INST_STB}

	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov UP, DOWN

	# read reg dst
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_STB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov DOWN, RIGHT
	mov ${OP_NIL}, RIGHT

	# push src addr
	mov ACC, DOWN

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL
	
	# read reg src
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_STB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov DOWN, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, DOWN
	mov UP, NIL

	# write memory [dst]
	sav
	shr 6
	add ${ADDR_MEMORY_BASE}
	mov ACC, RIGHT
	swp
	mov ${ADDR_INST_STB}, RIGHT
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
	mov ${ADDR_INST_STB}, RIGHT
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
	mov UP, UP
	mov UP, UP
	mov ACC, UP
end
