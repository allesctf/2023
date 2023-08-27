package challenges

challenges: "note-pad": {
	enabled:		true
	displayName:	"Awesome Notepad"
	category:	   "Web"
	difficulty:	 "Easy"
	author:		 "explo1t"
	broker:		 "note-pad"
	brokerProtocol: "https"

	description: """
		I created *cough copied cough* a fancy new shared Notepad. If you find any issue just report it to me via the bug button. I will regularly check for any new issues, but i bet you will not find any ;)

		Infrastructure hint: Our infrastructure uses a shared network namespace. All pods for this challenge are reachable via localhost on different ports, not via the container hostnames.
		"""
	deployment: {
		containers: [
			{
                image: "note-pad-app", 
                buildRoot: "deploy/note-pad",
                env: {
					"SESSIONID" : "$SESSIONID",
					"CHALLENGE_DOMAIN" : "$CHALLENGE_DOMAIN",
					"REACT_APP_ROOT":"http://localhost:1024",
					"TICKET_APP_API":"http://localhost:4000",
					"TICKET_APP_ROOT":"http://localhost:8000"
                }
            },
			{
                image: "note-pad-api", 
                buildRoot:     "deploy/note-pad-api"
            },
			{
                image: "note-pad-nginx", 
                buildRoot:     "deploy/note-nginx"
            },
			{
                image: "note-pad-admin", 
                buildRoot: "deploy/note-admin",
                env: {
                   "SESSIONID" : "$SESSIONID",
					"CHALLENGE_DOMAIN" : "$CHALLENGE_DOMAIN",
					"REACT_APP_ROOT":"http://localhost:1024",
					"TICKET_APP_API":"http://localhost:4000",
					"TICKET_APP_ROOT":"http://localhost:8000"
                }
            },
			{
                image: "note-pad-browser", 
                buildRoot: "deploy/note-browser",
                env: {
                    "SESSIONID" : "$SESSIONID",
					"CHALLENGE_DOMAIN" : "$CHALLENGE_DOMAIN",
					"REACT_APP_ROOT":"http://localhost:1024",
					"TICKET_APP_API":"http://localhost:4000",
					"TICKET_APP_ROOT":"http://localhost:8000"
                }
            }
		]
		ports: [{
			type:         "sni_proxy"
			port:         1024
			name:         "app-service"
			displayStyle: "https"
		}]
		
		networkPolicies: ["allow-outgoing"]
	}

	points: 100
	flag:   "ALLES!{s3cr37_mu7a710n5_4r3_a_f347ur3_n07_4_bu6}"

	files: [{
		name:      "notepad.zip"
		sha256sum: "0cc604cb7045d7c00ab188e3f3925bf1575e6be6594cf740f1f00d4a29eb50f3"
	}]
}
