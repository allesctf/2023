package challenges

challenges: "seebeesee": {
	enabled:     true
	displayName: "SeeBeeSee"
	category:    "Crypto"
	difficulty:  "Easy"
	author:      "r0bre"
	broker:      "seebeesee"

	description: """
		I came up with this great idea for securely running scripts on my testing server by using cryptography!
		"""

	deployment: {
		containers: [{
			image: "seebeesee"
		}]
	}

	points: 100
	flag:   "ALLES!{1m_n3ver_us1ng_cbc_4gaiN!!!1}"

	files: []
}
