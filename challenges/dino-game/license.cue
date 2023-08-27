package challenges

challenges: "license": {
	enabled:     true
	displayName: "License"
	category:    "Game Hacking"
	difficulty:  "Hard"
	author:      "localo",
	broker:      "game-server",


	description: """
		Reverse Engineering in Python? Not possible they say. Luckily, dinos know how to use native Python modules!
		"""


	deployment: {
		containers: [
			{
                image: "game-server", 
                buildRoot: "../dino-game/deploy",
				env: {
					"TEAM": "$TEAM"
				},
				build: false
			}
		]
		ports: [{
			type:         "sni_proxy"
			port:         1024
			name:         "app-service"
			displayStyle: "netcat"
		}]
		
		networkPolicies: ["game"]
	}

	points: 100
	flag:   "ALLES!{Damn_even_with_CFO!?}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
