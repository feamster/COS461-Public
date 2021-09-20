#!/bin/bash

# script for setting up the environment on ubuntu 14.04

sudo apt-get update
sudo apt-get install -y emacs
cp ./config_files/dot_emacs ~/.emacs
sudo apt-get install -y python-dev python-pip
# Build Python 2.7.12 from source
sudo apt-get install -y build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev
wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
tar -xf Python-2.7.12.tgz
cd Python-2.7.12
./configure
make && sudo make install
cd .. && rm -f Python-2.7.12.tgz && rm -rf Python-2.7.12

# get pip
curl -O https://bootstrap.pypa.io/pip/2.7/get-pip.py
sudo python get-pip.py
rm -f get-pip.py

# install go
sudo apt-get install -y gccgo-go
# Install old version of tornado before installing jupyter
sudo pip install tornado==4.5.3
sudo pip install jupyter
sudo pip install tzupdate==1.5.0

# Set correct permissions for bash scripts
find . -name "*.sh" | xargs chmod -v 744

# If the repository was pulled from Windows, convert line breaks to Unix-style
sudo apt-get install -y dos2unix
printf "Using dos2unix to convert files to Unix format if necessary..."
find . -name "*" -type f | xargs dos2unix -q

# Assignment 2
sudo pip install mininet
sudo pip install nbconvert
sudo pip install numpy
sudo pip install matplotlib
sudo apt-get install -y mininet
sudo apt-get install -y python-numpy
sudo apt-get install -y python-matplotlib
mkdir ~/.jupyter
cp ./config_files/jupyter_notebook_config.py ~/.jupyter/jupyter_notebook_config.py
jupyter_path=$(readlink -f .)
jupyter_path=${jupyter_path//\//\\\/}
sed -i "s/\/vagrant/${jupyter_path}/g" ~/.jupyter/jupyter_notebook_config.py
# uncomment below if using ubuntu 16.04
# sudo apt-get install -y openvswitch-testcontroller
# sudo ln /usr/bin/ovs-testcontroller /usr/bin/ovs-controller 
# sudo kill $(pidof ovs-testcontroller)

# startup script 
sudo bash -c 'cat << EOF > /etc/init/cos461.conf
description "For cos461 assignments"
start on startup
task
script
    modprobe tcp_probe port=5001 full=1
end script
EOF'

sudo tzupdate 
sudo modprobe tcp_probe port=5001 full=1

# Assignment 3
sudo apt-get install -y whois
sudo pip install ipaddress

# Assignment 5
sudo apt-get install -y apache2-utils
echo "export GOPATH=$(readlink -f assignment5)" >> ~/.profile

# Start in the assignments dir instead of ~/
if ! grep -Fxq "cd $(readlink -f .)" ~/.bashrc
then
    echo "cd $(readlink -f .)" >> ~/.bashrc
fi
