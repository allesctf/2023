#!/bin/sh


for f in test/*.asm; do
	in="$(echo "$f" | cut -d. -f1).in"
	out="$(echo "$f" | cut -d. -f1).out"
	tmp="/tmp/tis-test.out"
	./tis-as "$f" "$in" "$tmp"
	if [ $? -ne 0 ]; then
		echo "$f"
	elif ! diff "$out" "$tmp"; then
		cat "$tmp" | xxd 1>&2
		cat "$out" | xxd 1>&2
		echo "$f"
	fi
done
