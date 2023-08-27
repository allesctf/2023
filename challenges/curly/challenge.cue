package challenges

challenges: "curly": {
	enabled:     true
	displayName: "Curly"
	category:    "Pwn"
	difficulty:  "Easy/Medium"
	author:      "Flo"
	broker:      "curly"

	description: """
	Curl's C API is [easy and fun](https://curl.se/libcurl/c/). Try it out today, you might even find a flag. :)
	"""

	points: 200
	flag:   "ALLES!{might_as_well_add_CURLOPT_RUN_SYSTEM}"
	deployment: {
		containers: [{ image: "curly" }]
		ports: [{
			type: "sni_proxy",
			port: 1024,
			name: "app-service",
			displayStyle: "netcat"
		}]
		networkPolicies: ["allow-outgoing"]
	}

	files: []
}
