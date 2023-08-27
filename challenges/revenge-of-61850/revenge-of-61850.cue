package challenges

challenges: "revenge-of-61850": {
	enabled:     true
	displayName: "Revenge of the libiec61850"
	category:    "Pwn"
	difficulty:  "Medium"
	author:      "0x4d5a"
	brokerProtocol: "ssh"
	broker:      "revenge-of-61850"


	description: """
		The CSCG qualification, a big german hacking competition, featured the challenge `Honk! Honk!`, exploiting the `GOOSE` server of the [libiec61850](https://github.com/mz-automation/libiec61850). Now, it is not "Honk Honk!" anymore. You still need to exploit a 0-day in the libiec61850, but this time in the libiec61850 client. 

		Some notes:
		 - You will get access to a server via SSH. You can even use SCP to upload your exploit.
		 - Every second, the following command will run as root: `./mms_utility -p 1337 -d -i -f -m`
		 - If you have problems to SCP your exploit into the container, try `scp -P 31222 -O [...]`. 
		"""

	deployment: {
		containers: [{
			image: "revenge-of-61850"
		}]

	}

	files: [{
        name:      "revenge-of-61850.zip"
        sha256sum: "f818f450d011c42bd8088cc3e282a2437bbb6ffaec7001f49569e6145d546fb2"
    }]

	points: 100
	flag:   "ALLES!{Y3s_th3_client_st1ll_h4s_many_vulns}"
}
