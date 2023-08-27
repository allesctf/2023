package challenges

challenges: "stegosaurus": {
	enabled:     true
	displayName: "Stegosaurus"
	category:    "Game Hacking"
	difficulty:  "Guessy"
	author:      "D_K",
	broker:      "game-server",


	description: """
		In todays world, we hide secrets with crypto. I wonder what they did back in the dinosaur age. I think those secrets are hidden below the earth today.

		Hint: You don't need any public stego tooling for this task
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
	flag:   "ALLES!{Jur4ss1cCrypto}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
