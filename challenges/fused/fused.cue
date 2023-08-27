package challenges

challenges: "fused": {
	enabled:     true
	displayName: "FusEd"
	category:    "Crypto"
	difficulty:  "Medium"
	author:      "Nevsor"
	broker:      "fused"

	description: """
	Programming microcontrollers is too complicated. How about an (emulated) MCU that can directly execute Python code?
	"""

	deployment: {
		containers: [{
			image: "fused"
		}]
	}

	points: 200
	flag:   "ALLES!{inspired by the RoT verification of the LPC54S0xx, cf. https://www.nxp.com/docs/en/application-note/AN13390.pdf}"

	files: [{
		name:      "FusEd.zip"
		sha256sum: "10e32cf7dd8ea338c976771a7ee57590ac9dd81732dea32c33891ec0102c836c"
	}]
}
