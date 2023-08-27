package challenges

challenges: "plugin-manager": {
	enabled:     true
	displayName: "Plugin Manager"
	category:    "Pwn"
	difficulty:  "Medium"
	author:      "0x4d5a"
	brokerProtocol: "ssh"
	broker:      "plugin-manager"


	description: """
		I'm a hacker (Kali = ❤️) with a big company enterprise background (.NET = ❤️). So I combined my skills and build a cool plugin manager.

		Mono is missing Code Access Security and proper authenticode support, but I managed to verify my signed and trusted plugins anyway. 

		Some notes:
		 - You will get access to a server via SSH. You can even use SCP to upload your exploit.
		 - Use the setuid binary `./run_wrapper` to start the plugin manager
		"""

	deployment: {
		containers: [{
			image: "plugin-manager"
		}]

	}


	points: 100
	flag:   "ALLES!{m0n0=dotNET_and_unix_b3st_0f_tw0_worlds!}"

	files: [{
		name:      "plugin-manager.zip"
		sha256sum: "ebef7bcde1012d5b1ca8586261f447d47be7a6fdd4ca5d7d925ba23520840f08"
	}]
}
