package challenges

challenges: "sanity-check": {
	enabled:     true
	displayName: "Sanity Check"
	category:    "Game Hacking"
	difficulty:  "Baby"
	author:      "0x45da",
	broker:      "game-server",

	description: """
		Talk to Kuro and learn about this wonderful dino land you landed in.

		Before you can do that, you have to get the client (and local server) running. Here are some primers to get started:
		
		- We use poetry to manage the python venv and all dependencies. Check out the [poetry docs](https://python-poetry.org/docs/) how to install poetry
		- You need python >= 3.10, otherwise the game won't start
		- Use `poetry install` in the root directory to do all the magic.
		- If you use Ubuntu, poetry might being stuck resolving dependencies. Disabling they keyring support might solve this: `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` before `poetry install`
		- If you encounter errors regarding `*.gif` animations when starting the game, make sure to install `gdk-pixbuf` and `gdk-pixbuf-xlib` (or use the nix flake)

		After installation, check out the `README.md` to get the server running. The server allows you to better understand the game, but has some limitations:

		- You only get access to a test map in JSON format
		- The flags are redacted (duh)
		- Some modules are missing, like the source code of the `native` folder

		**Note: You can't use `ncat` to connect to the game server directly. Use the game client instead. The `ncat` command below is just for copy and paste convenience. Read the `README.md` for further instructions!**
		"""


	deployment: {
		containers: [
			{
                image: "game-server", 
                buildRoot: "../dino-game/deploy",
				env: {
					"TEAM": "$TEAM"
				}
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
	flag:   "ALLES!{w3lc0me_to_din0_land}"
	files: [{
		name:      "camp_gamedev-public.zip"
		sha256sum: "db40778dc6d6c3a70a0aa12c92fad293a7176d5005538022183d590bef27d535"
	}]
}
