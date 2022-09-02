#!/usr/bin/env bash

# cd into the basedir
BASEDIR=$(dirname "$0")
cd $BASEDIR

# Confirm
read -p "Hello, this script pulls from git and redeploys the bot using pm2. Would you like to continue? (y/N) " -n 1 -r
echo 

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # The user agreed
    git pull
    pm2 restart discord-test-your-luck

    if [ -f uses.txt ]
    then
        echo "Uses.txt already exists! Skipping!"
    else
        read -p "It looks like you are missing uses.txt, would you like to create it? (y/N) " -n 1 -r
        echo
        touch "uses.txt"
        echo "0" > "uses.txt"

fi