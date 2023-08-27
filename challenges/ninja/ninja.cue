package challenges

challenges: "ninja": {
	enabled:     true
	displayName: "Ninja"
	category:    "Outdoor"
	difficulty:  "Easy"
	author:      "pony, blue, d_k"

	description: """
		This challenge is almost impossible. You must bridge the air gap (look for the climbing assembly at [https://osm.org/go/0Mc_ekY7l--?m=](https://osm.org/go/0Mc_ekY7l--?m=) ) and infiltrate the airgapped device. The device in question is a standard Pi OS installation with a tiny script that gets autoexecuted whenever a USB stick is plugged in.
		```bash
		#!/bin/bash
		set -e;
		mount /dev/sd*1 /mnt;
		cp /home/pony/The_Super_Secret_Flag.txt /mnt/;
		umount /mnt;
		```

		Yes, you read that right. The device will hack itself and automatically give you the flag... if you can reach it.  :P

		Location: [https://osm.org/go/0Mc_ekY7l--?m=](https://osm.org/go/0Mc_ekY7l--?m=)

		You can come from 17. at ~9:00 until Saturday ~11:00 AM.
		"""

	points: 0
	flag:   "ALLES!{Well done, young ninja. You have mastered the first of many trials. Present your prize to sensei, and you shall enter the next stage of your training.}"

	files: []
    badge_id: "ninja"
}
