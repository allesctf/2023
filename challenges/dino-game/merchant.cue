package challenges

challenges: "merchant": {
	enabled:     true
	displayName: "Merchant"
	category:    "Game Hacking"
	difficulty:  "Medium"
	author:      "D_K",
	broker:      "game-server",


	description: """
		Throwback to the Great Exchange north of Varrock in RuneScape. If you got the best trades back then, you will have no issues to make some profit and buy the flag.
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
	flag:   "ALLES!{Arbitrage_and_st0nks!:chart_with_upwards_trend:}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
