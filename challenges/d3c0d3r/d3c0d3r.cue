package challenges

challenges: "d3c0d3r": {
	enabled:     true
	displayName: "d3c0d3r"
	category:    "Misc"
	difficulty:  "Easy"
	author:      "0x4d5a"
	broker:      "d3c0d3r"

	description: """
	d3c0d3r time it is :)
	"""

	deployment: {
		containers: [{
			image: "d3c0d3r"
		}]
	}

	points: 100
	flag:   "ALLES!{why_w0uld_any0n3_1mplem3nt_such_a_pr1mit1ve?-.-}"

	files: [{
		name:      "d3c0d3r.zip"
		sha256sum: "c6b94d84f2f4de7119a6595be6c876dff6512a50d44cfa62b14c0b94c703286f"
	}]
}
