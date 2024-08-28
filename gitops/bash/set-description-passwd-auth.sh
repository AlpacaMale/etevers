#!/usr/bin/bash

for HOST in servera serverb serverc
do
        ssh ${HOST} sudo "sed -i -E 's/PasswordAuthentication yes/# &/' /etc/ssh/sshd_config"
        ssh ${HOST} sudo "sed -i -E 's/PermitRootLogin yes/# &/' /etc/ssh/sshd_config"
        ssh ${HOST} sudo systemctl restart sshd
done

exit 0
