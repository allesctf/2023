stdin X0 Y0 DOWN

tpu X0 Y0
	## ${ADDR_INST_INP}

	# get req
	mov UP, LEFT
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL
	sav

	# get input
	mov DOWN, ACC
	swp

	# write reg
	mov ${ADDR_GPR}, RIGHT
	mov ${ADDR_INST_INP}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov ACC, RIGHT
	swp
	mov ACC, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	# send ACK
	mov LEFT, RIGHT
	mov ${ADDR_INST_INP}, RIGHT
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
