#!/usr/bin/bash
ls -l /home/prajwal
read -p 'Enter Filename to share: ' filename
read -p 'Enter receiver username: ' user
read -p 'Enter receiver hostname: ' ip
if [[ $filename = encrypted* ]]
then
	scp $filename $user@$ip:/home/$user/
else
	echo "Invalid Filename"
fi
