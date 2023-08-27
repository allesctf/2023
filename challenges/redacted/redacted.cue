package challenges

challenges: "redacted": {
	enabled:     true
	displayName: "Redacted"
	category:    "Misc"
	difficulty:  "Easy"
	author:      "Nevsor"

	description: """
		Oops, I almost leaked my s3cret data. But all good.

		*Note: This challenge has a different flag format, cause changing the flag is hard...*
		"""


    files: [{
        name:      "redacted.jpg"
        sha256sum: "5d428f8418cfad628852b5e1110902c28a4d084b0579c63d4f2ce61d0f7a9dbe"
    }]
	points: 100
	flag:   "CSCG{why_tf_did_ParcelFileDescriptor.parseMode_in_Android_10_change_the_meaning_of_\"w\"_mode?_https://issuetracker.google.com/issues/180526528}"
}
