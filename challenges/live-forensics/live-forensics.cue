package challenges

challenges: "live-forensics": {
	enabled:     true
	displayName: "live-forensics"
	category:    "Forensics"
	difficulty:  "Medium"
	author:      "d0ntrash"
	brokerProtocol: "ssh"
	broker:      "live-forensics"

	description: """
		We have detected suspicious network traffic originating from one of our servers. Could you assist us in investigating this? Hopefully, we won't become the next victim of the Iron Oxide Infiltrators!
		"""

	deployment: {
		containers: [{
			image: "live-forensics"
		}]

		networkPolicies: ["allow-outgoing"]

	}

	points: 100
	flag:   "ALLES!{Th3_p4s5w0rd_i5_'infected'!}"
}