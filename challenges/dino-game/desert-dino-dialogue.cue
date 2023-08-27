package challenges

challenges: "desert-dino-dialogue": {
	enabled:     true
	displayName: "Desert Dino Dialogue"
	category:    "Game Hacking"
	difficulty:  "Easy"
	author:      "D_K",
	broker:      "game-server",


	description: """
	Welcome to the "Desert Dino Dialogue" challenge, where you will embark on a unique and captivating encounter in the scorching desert. Deep within the arid landscape, hidden behind towering mountains, resides a lonely NPC (Non-Player Character) like no other—a talking dinosaur longing for a conversation.

	Your task is to engage in an extended conversation with this fascinating desert-dweller. The dinosaur, with its ancient wisdom and boundless tales, awaits someone who can listen patiently and provide companionship. As the sweltering sun beats down upon the desert, only the most persevering challengers will succeed in breaking through the dinosaur's initial reserve to unearth its treasure trove of knowledge.

	The key to this challenge lies in building a rapport with the dinosaur. Though initially wary and hesitant, it will gradually warm up to you as you demonstrate genuine interest and empathy. The NPC's experiences span centuries, ranging from tales of long-lost civilizations to the secrets of survival in the unforgiving desert. Show your dedication, and it will reveal hidden clues that can be utilized in future challenges.

	As you converse with the dinosaur, be mindful of the surrounding environment. The desert can be treacherous, with blistering winds, sandstorms, and dangerous wildlife. Maintain your focus and stay resilient, for every conversation carries the potential to unlock new avenues of exploration.

	Remember, the objective of this challenge is to establish a meaningful connection with the dinosaur by actively listening and engaging in a dialogue. Patience and perseverance are the keys to success in unraveling the secrets of the desert and earning the respect of this ancient creature.

	Are you ready to delve into the heart of the desert, behind the mountains, to converse with the last remaining dinosaur? Prepare yourself for a journey of discovery, where a simple conversation may hold the key to untold mysteries and open doors to unimaginable possibilities.

	Good luck, brave challenger! The desert awaits your arrival, and the dinosaur yearns for someone to share its stories with.
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
	flag:   "ALLES!{L0n3ly_D1n0sp34k1ng1n_D3s3rt}"
		files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
