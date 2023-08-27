package challenges

challenges: "ransomware": {
	enabled:     true
	displayName: "Ransomware"
	category:    "Reverse Engineering"
	difficulty:  "Easy"
	author:      "lion"

	description: """
		Oh no! I got hit by one of those infamous flag encrypting ransomwares for linux. Luckily it crashed. Can you help me recover my files?
		"""

	points: 100
	flag:   "ALLES!{Pls_send_1btc_to_bc1a1y2kgayajvsqbzbanayr2244a5a3aafa1a0w2h_for_extra_points}"

	files: [{
		name:      "ransomware.zip"
		sha256sum: "f501c4a3b78935fcb3f23f4f7d203b630501ea3b29515ab2473dfd7a8b5aad20"
	}]
}
