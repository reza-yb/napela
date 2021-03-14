#!/bin/bash

apt update -qy
apt install -y ruby-dev

gem install dpl
dpl --provider=heroku --app=$1 --api-key=$2

