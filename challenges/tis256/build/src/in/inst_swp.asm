tpu X0 Y0
	## ${ADDR_INST_SWP}

	# get req
	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov ACC, DOWN
	mov UP, DOWN

	# read reg src
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SWP}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack (src value)
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# write reg dst
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SWP}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov DOWN, RIGHT
	mov ACC, RIGHT

	# get ack (prev dst value)
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# write reg src
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SWP}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov DOWN, RIGHT
	mov ACC, RIGHT

	# get ack (prev src value)
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	# send ack
	mov DOWN, RIGHT
	mov ${ADDR_INST_SWP}, RIGHT
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
	mov UP, UP
	mov ACC, UP
	swp
	mov ACC, UP
end
