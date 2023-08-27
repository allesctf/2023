package challenges

challenges: "unreachable": {
	enabled:     true
	displayName: "Unreachable"
	category:    "Game Hacking"
	difficulty:  "Medium"
	author:      "localo",
	broker:      "game-server",


	description: """
		Oopsie woopsie, I somehow managed to loose a flag while working on the map, I will remove when I find it again in a day or two.
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
	flag:   "ALLES!{cyberpunk_dev_at_work}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
