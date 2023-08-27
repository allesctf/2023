tpu X0 Y0
	## ${ADDR_TESTER}

	mov ${ADDR_INST_SHL}, RIGHT
	mov ${ADDR_TESTER}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov 0x00, RIGHT
	mov 4, RIGHT

	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	mov ${ADDR_INST_SHR}, RIGHT
	mov ${ADDR_TESTER}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov 0x01, RIGHT
	mov 2, RIGHT

	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	${HLT}
end

tpu X1 Y0
	mov LEFT, UP
end
