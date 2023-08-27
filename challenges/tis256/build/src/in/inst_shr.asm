tpu X0 Y0
	## ${ADDR_INST_SHR}

	# get req
	mov UP, DOWN
	mov UP, NIL
	mov UP, ACC
	mov UP, DOWN

	# get register
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SHR}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# save src addr
	mov ACC, DOWN

	# get resp
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# shift value
	shr DOWN

	# set register
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_SHR}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov DOWN, RIGHT
	mov ACC, RIGHT

	# get resp
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	# send ack
	mov DOWN, RIGHT
	mov ${ADDR_INST_SHR}, RIGHT
	mov ${OP_ACK}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT
end

tpu X1 Y0
	mov LEFT, UP
end

tpu X0 Y1
	mov UP, DOWN
	mov UP, ACC
	mov UP, DOWN
	mov ACC, UP
	mov DOWN, UP
	mov DOWN, UP
end

tpu X0 Y2
	mov UP, ACC
	mov UP, UP
	mov ACC, UP
end
