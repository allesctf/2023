tpu X0 Y0
	## ${ADDR_TESTER}

	mov ${ADDR_INST_MOV}, RIGHT
	mov ${ADDR_TESTER}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov 0x00, RIGHT
	mov 0x01, RIGHT

	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	mov ${ADDR_INST_SWP}, RIGHT
	mov ${ADDR_TESTER}, RIGHT
	mov ${OP_NIL}, RIGHT
	mov 0x02, RIGHT
	mov 0x03, RIGHT

	mov UP, NIL
	mov UP, NIL
	mov UP, NIL
	mov UP, NIL

	${HLT}
end

tpu X1 Y0
	mov LEFT, UP
end
