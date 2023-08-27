package challenges

challenges: "navity": {
        enabled:        true
        displayName:    "Navity"
        category:       "Misc"
        difficulty:     "Easy"
        author:         "localo"
        broker:         "navity"

        description: """
                I made this cool bare metal arm firmware that can calculate a the fib number for a given input. You have to use `ncat -C` to talk to the application. 

                You can also connect to another exposed port by changing the ncat command. 

                `ncat -C --ssl 84d765a3391925f34bbb1223-1024-navity.challenge.master.camp.allesctf.net 31337` -> `ncat -C --ssl 84d765a3391925f34bbb1223-1234-navity.challenge.master.camp.allesctf.net 31337` to connect to port 1234.

                You have to create a new session after each run :)
                """
        deployment: {
        containers: [{
                image: "navity"
        }]
        ports: [
        {
                type: "sni_proxy",
                port: 1024,
                name: "app-service",
                displayStyle: "netcat"
        },
        {
                type: "sni_proxy",
                port: 1234,
                name: "gdb-service",
                displayStyle: "netcat"
        },
        ],
        }

    files: [{
        name:      "navity.zip"
        sha256sum: "2d1d4224a000078f7f4a992c7b07e06830feb143f3d8b46ec819b262edb5dfc7"
    }]

        points: 100
        flag:   "ALLES!{it's_not_a_bug_it's_a_feature_?xD}"
}
