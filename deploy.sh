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
fi