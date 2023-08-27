tpu X0 Y0
	## ${ADDR_CPU}

	# read rip
	mov ${ADDR_RIP}, RIGHT
	mov ${ADDR_CPU}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov 0x00, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL

	# read inst
	sav
	shr 6
	add ${ADDR_MEMORY_BASE}
	mov ACC, RIGHT
	swp
	mov ${ADDR_CPU}, RIGHT
	mov ${MEM_OP_READ}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	swp
	mov UP, NIL
	mov UP, NIL
	mov UP, ACC
	mov UP, NIL
	swp

	# write rip+1
	add 1
	mov ${ADDR_RIP}, RIGHT
	mov ${ADDR_CPU}, RIGHT
	mov ${MEM_OP_WRITE}, RIGHT
	mov 0x00, RIGHT
	mov ACC, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	swp

	# run inst
	mov ${ADDR_DECODER}, RIGHT
	mov ${ADDR_CPU}, RIGHT
	mov ACC, RIGHT
	mov ${OP_NIL}, RIGHT
	mov ${OP_NIL}, RIGHT

	# get ack
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
end

tpu X1 Y0
	mov LEFT, UP
end
