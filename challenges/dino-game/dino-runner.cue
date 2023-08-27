package challenges

challenges: "dino-runner": {
	enabled:     true
	displayName: "Dino Runner"
	category:    "Game Hacking"
	difficulty:  "Hard"
	author:      "localo",
	broker:      "game-server",


	description: """
		Ohh no. It seems your internet breaks once you talk to beautiful Disconnecta. Get a highscore of at least 1337 points, impress Disconnecta and obtain the flag.
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
	flag:   "ALLES!{snap!Back_to_reality!But_there_is_still_gravity:(}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
