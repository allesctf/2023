package challenges

challenges: "tis256": {
	enabled:     true
	displayName: "TIS-256"
	category:    "Reverse Engineering"
	difficulty:  "Hard"
	author:      "sinitax"

	description: """
		pff -- password managers, I verify secrets with a TPM! (tesselated platform module)
		"""

	points: 200
	flag:   "ALLES!{T3553L4T3!}"

	files: [{
		name:      "tis256.zip"
		sha256sum: "ab8f706cf20f35572d48cfe5cf4cca73e49edf2d96082f1744961fe39bd3132d"
	}]
}
