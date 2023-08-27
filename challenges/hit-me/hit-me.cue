package challenges

challenges: "hit-me": {
	enabled:     true
	displayName: "Hit Me"
	category:    "Pwn"
	difficulty:  "Medium"
	author:      "lion"
	broker:      "hit-me"

	description: """
		I made a game. Just for you <33. Hope you like it.
		"""

	deployment: {
		containers: [{
			image: "hit-me"
		}]
	}

	points: 200
	flag:   "ALLES!{0h_n0E5..l000k5_L1ke_y0U_M155ed:((}"

	files: [{
		name:      "hit-me.zip"
		sha256sum: "3382342ae6545ef08be60ddc78ea3070fb6b13d8328e44183e520e971a5dc925"
	}]
}
