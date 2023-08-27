package challenges

challenges: "dash-dash-execute": {
	enabled:     true
	displayName: "--x"
	category:    "Misc"
	difficulty:  "Easy"
	author:      "Flo"
	broker:      "dash-dash-execute"
	brokerProtocol: "ssh"

	description: """
	Did you know that you can mark executables as non-readable? Check out `/usr/bin/flagcheck` for an example.
	"""

	deployment: {
		containers: [{ image: "dash-dash-execute" }]
	}

	points: 100
	flag:   "ALLES!{surprisingly_similar_to_setuid_processes_but_not_actually_secure}"

	files: [{
		name: "flagcheck.c"
		sha256sum: "9295128211f0d55235bbae7980daf44884b5d52ea0e6446d41d60e64efa54c24"
	}]
}
