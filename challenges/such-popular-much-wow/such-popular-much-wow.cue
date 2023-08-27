package challenges

challenges: "such-popular-much-wow": {
	enabled:		true
	displayName:	"Such popular, much wow"
	category:	   "Web"
	difficulty:	 "Medium"
	author:		 "0x4d5a"
	broker:		 "diff-the-patch"
	brokerProtocol: "https"

	description: """
		I heard you like web challenges with sourcecode provided. Lets find a simple 0-day in an old and vulnerable plugin.

		Take a look at the `entry-point.sh` script. You'll find helpful credentials in there.
		"""
	deployment: {
		containers: [
			{
                image: "such-popular-much-wow-wordpress", 
                buildRoot: "deploy/wordpress",
                env: {
                    "WORDPRESS_DB_HOST": "127.0.0.1",
                    "WORDPRESS_DB_USER": "exampleuser",
                    "WORDPRESS_DB_PASSWORD": "examplepass",
                    "WORDPRESS_DB_NAME": "wpdb",
                    "ADMINPW": "eqmfz1aMXGsGe3cyLeos!",
                    "WORDPRESS_PORT": "31337",
					"SESSIONID" : "$SESSIONID",
					"CHALLENGE_DOMAIN" : "$CHALLENGE_DOMAIN"
                }
            },
			{
                image: "such-popular-much-wow-mysql", 
                buildRoot:     "deploy/mysql",
                 env: {
                    "MYSQL_DATABASE": "wpdb",
                    "MYSQL_USER": "exampleuser",
                    "MYSQL_PASSWORD": "examplepass",
                    "MYSQL_RANDOM_ROOT_PASSWORD": "1"
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

	points: 200
	flag:   "ALLES!{Sn3aky_B3aky_HTML_enc0de_t0_d3c0de.Why_th0ugh?:thinking:}"

	files: [{
		name:      "such-popular-much-wow.zip"
		sha256sum: "9d055d6a6868d03f92ec763282c9fd76faa8ef56d8bbd305d4c1f6176343de7c"
	}]
}
