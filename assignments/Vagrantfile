# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure(2) do |config|

  # 64 bit Ubuntu Vagrant Box
  config.vm.box = "ubuntu/trusty64"

  ## Configure hostname and port forwarding
  config.vm.hostname = "cos461"
  config.ssh.forward_x11 = true
  config.vm.network "forwarded_port", guest: 8888, host: 8888
  # Assignment 7
  config.vm.network "forwarded_port", guest: 12000, host: 12000

  vagrant_root = File.dirname(__FILE__)

  # Emacs settings
  config.vm.provision "file", source: "#{vagrant_root}/config_files/dot_emacs", destination: "~/.emacs"

  # Jupyter notebook settings
  config.vm.provision "file", source: "#{vagrant_root}/config_files/jupyter_notebook_config.py", destination: "~/.jupyter/jupyter_notebook_config.py"

  ## Provisioning
  config.vm.provision "shell", inline: <<-SHELL
     # Assignment 1
     sudo apt-get update
     sudo apt-get -y upgrade
     sudo apt-get install -y emacs
     sudo apt-get install -y python-dev
     curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
     sudo python get-pip.py
     rm -f get-pip.py
     # Install old version of tornado before installing jupyter
     sudo pip install tornado==4.5.3
     sudo pip install jupyter
     sudo apt-get install -y gccgo-go
     sudo pip install -U tzupdate
     echo "export PYTHONPATH=${PYTHONPATH}:/vagrant/course-bin" >> /home/vagrant/.profile

     # Set correct permissions for bash scripts
     find /vagrant -name "*.sh" | xargs chmod -v 744

     # If the repository was pulled from Windows, convert line breaks to Unix-style
     sudo apt-get install -y dos2unix
     printf "Using dos2unix to convert files to Unix format if necessary..."
     find /vagrant -name "*" -type f | xargs dos2unix -q

     # Assignment 2
     sudo apt-get install -y python-tk

     # Assignment 3
     sudo pip install nbconvert
     sudo apt-get install -y mininet
     sudo apt-get install -y python-numpy
     sudo apt-get install -y python-matplotlib

     # Assignment 4
     sudo apt-get install -y whois
     sudo pip install ipaddress

     # Assignment 6
     sudo pip install scapy
     sudo apt-get install -y python-scipy
     sudo apt-get install -y bind9
     sudo cp /vagrant/assignment6/bind/* /etc/bind

     # Assignment 7
     sudo apt-get install -y apache2-utils
     echo "export GOPATH=/vagrant/assignment7" >> /home/vagrant/.profile

     # Start in /vagrant instead of /home/vagrant
     if ! grep -Fxq "cd /vagrant" /home/vagrant/.bashrc
     then
      echo "cd /vagrant" >> /home/vagrant/.bashrc
     fi
  SHELL

  ## Provisioning to do on each "vagrant up"
  config.vm.provision "shell", run: "always", inline: <<-SHELL
    sudo tzupdate 2> /dev/null
    # Assignment 3
    sudo modprobe tcp_probe port=5001 full=1
  SHELL

  ## CPU & RAM
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "100"]
    vb.memory = 2048
    vb.cpus = 1
  end

end
