#!/usr/bin/bash
for HOST in servera serverb serverc
do
	ssh ${HOST} sudo hostnamectl set-hostname ${HOST}
done

exit 0
