tpu X0 Y0
	## ${ADDR_INST_SUB}

	# get req
	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov UP, DOWN

	# read reg src
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SUB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# read reg dst
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SUB}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov DOWN, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	sub UP
	mov UP, NIL
	neg

	# write reg
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SUB}, RIGHT
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
	mov ${ADDR_INST_SUB}, RIGHT
	mov ${OP_ACK}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT
end

tpu X1 Y0
	mov LEFT, UP
end

tpu X0 Y1
	mov UP, ACC
	swp
	mov UP, ACC
	mov ACC, UP
	mov ACC, UP
	swp
	mov ACC, UP
end
