package challenges

challenges: "babyrsa": {
	enabled:     true
	displayName: "Baby RSA"
	category:    "Crypto"
	difficulty:  "Medium"
	author:      "floesen"

	description: """
	I stumbled across this weird RSA implementation. However, it seems like it still works correctly. Can you figure out how? The flag is contained in one of the prime factors of N!
	"""

	points: 200
	flag:   "ALLES!{c0ngr4tZ_y0u_br0K3_A_Wh1t3b0x_RSA_1mpL3m3nt4t10n}"

	files: [{
		name: "babyrsa.zip"
		sha256sum: "7a93e1694a4c9ff8a4b3920481d9cdba4188760fd78a3a197a49ba9711ddebca"
	}]
}
