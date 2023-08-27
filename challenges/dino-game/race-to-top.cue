package challenges

challenges: "race-to-top": {
	enabled:     true
	displayName: "Race to the Top"
	category:    "Game Hacking"
	difficulty:  "Hard"
	author:      "D_K",
	broker:      "game-server",


	description: """
		Even dinos sometimes get lost. Find the lost dino and race to him as fast as possible. Otherwise, it might be to late!
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
	flag:   "ALLES!{l0st_and_f0und_1n_time}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
