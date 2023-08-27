package challenges

challenges: "dig-it-up": {
	enabled:     true
	displayName: "Dig It Up"
	category:    "Game Hacking"
	difficulty:  "Medium"
	author:      "localo",
	broker:      "game-server",


	description: """
		This task requires you blast [this song](https://www.youtube.com/watch?v=34CZjsEI1yU) in the background. Grab a shovel from Jones and dig up the flag!
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
	flag:   "ALLES!{I'm_a_dw4rf_and_1'm_D!GGING_A_HOLE}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
