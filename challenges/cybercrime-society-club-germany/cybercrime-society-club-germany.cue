package challenges

challenges: "cybercrime-society-club-germany": {
	enabled:     true
	displayName: "Cybercrime Society Club Germany"
	category:    "Web"
	difficulty:  "Easy"
	author:      "r0bre"
	broker:      "cybercrime-society-club-germany"
    brokerProtocol: "https"

    description: """
    You are agent Json Bourne. Your mission: Hack this new cybercrime website before it is too late.
    """

	deployment: {
		containers: [{
			image: "cybercime-society-club-germany"
		}]
        ports: [{
            type: "sni_proxy"
            port: 1024
            name: "app-service"
            displayStyle: "https"

               }]
	}

	points: 100
	flag:   "ALLES!{js0n_b0urn3_str1kes_ag4in!}"

    files: [{
        name: "cybercrime-society-club-germany.zip"
        sha256sum: "90c6faf7bc504df3bb922369e9c6ade310ef6ccd5e1279f604dbf272884ad428"
    }]
}
