stdout X0 Y0 DOWN

tpu X0 Y0
	## ${ADDR_INST_OUT}

	# get req
	mov UP, LEFT
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# read register value
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_OUT}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# receive response
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# output
	mov ACC, DOWN

	# send ACK
	mov LEFT, RIGHT
	mov ${ADDR_INST_OUT}, RIGHT
	mov ${OP_ACK}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT
end

tpu X1 Y0
	mov LEFT, UP
end

tpu X-1 Y0
	mov RIGHT, RIGHT
end
