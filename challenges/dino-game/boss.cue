package challenges

challenges: "boss": {
	enabled:     true
	displayName: "Boss"
	category:    "Game Hacking"
	difficulty:  "Easy"
	author:      "0x45da",
	broker:      "game-server",


	description: """
		The best kind of gamehacking: smash the overpowered boss enemy.

		George returned from his mountain vaccation and continues to roam the prehistoric earth, still causing troubles for CTF players. Get your revenge and beat him to death!
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
	flag:   "ALLES!{L3ss_annoying_th3n_qualifier_Ge0rge_right?}"
	files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
