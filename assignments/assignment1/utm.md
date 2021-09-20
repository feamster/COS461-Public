
## Setting up Virtual Machine for Apple Silicon Macs

COS 461 has been using VirtualBox+Vagrant to provide VM environment for the 
assignments. Unfortunately, VirtualBox does not support the newly released 
ARM-based Apple Silicon products (i.e., MacBook Pro with M1 chip). If you 
are using one of these products, please follow the instructions below for an 
alternative way of setting up the VM environment necessary for the assignments.

### Step 1: Download UTM

UTM is a virtualization software dedicated for macOS. UTM is backed by the 
QEMU emulator to provide VM support for both x86 Macs and ARM Macs. In 
addition, QEMU can emulate x86 VMs on ARM host machines and vice versa, 
though at reduced speed.

To download UTM, go to: https://mac.getutm.app to get the dmg disk image 
file, and then extract it to install the UTM application.

### Step 2: Import the VM image

We have prepared a [VM image for UTM](https://drive.google.com/file/d/17t-du78P7SNDzF3Br3Y9tquHhGptZSUG/view?usp=sharing) 
(You will need your Princeton credential to access the file).

After downloading the archive file to your Mac, double-click on it to extract 
the VM image file named `cos461.utm`. Then, open the UTM application, go to 
`File > Import Virtual Machine`, and select the utm image file to import the 
VM. Now in the UTM application, you should be able to see an entry for the 
imported VM in the left column. 

Now, you can click on the start button to boot up the VM. This will open up a 
window displaying VM startup information, and the startup is complete when it 
prompts for login. While you can log into the VM using the UTM window, it is 
highly recommended to use a separate terminal window and ssh into the VM. To 
do so, open up a terminal on your Mac and type the command 
`ssh -p2222 ubuntu@localhost` and then enter the password `ubuntu` to login.

To power off your VM, you can either run `sudo shutdown -h now` inside the VM 
or click on the poweroff button located at the top of the UTM window. To power 
cycle your VM, please shut it down first and then start it up again. The 
current version of UTM would crash if your run `sudo reboot` inside the VM.

(tip#1: By default, the VM is configured with 1 CPU core and 2GB RAM. Your VM 
could be slow since we are emulating an x86 machine on an ARM host. If your 
Mac has more than 2 cores and 4GB RAM, you can go to 
`Edit VM (top-right corner) > System` to increase RAM and the number of cores 
under Advanced Settings. You can do so only when your VM is powered off. 
Consuming half of your Mac's cores and RAM is recommended)

(tip#2: Sometimes your mouse might be trapped into the UTM window, press 
`option+command` to release it)

### Step 3: Clone course Git repository

ssh into the VM can run `git clone https://github.com/PrincetonUniversity/COS461-Public` 
to download the course files from GitHub.

`cd COS461-Public/assignments` to enter the course assignment directory.

### Step 4: Setup programming environment

Now run `./setup.sh` to setup the programming environment necessary for the 
assignments. This process could take up to 30 minutes to complete, depending 
on your VM hardware configuration. 

### Step 5: Go back to the main README and follow Part B

### Notes:

We are unable to find a seamless directory sharing solution for UTM. Unlike 
VirutalBox+Vagrant where the assignment directory is shared between the VM and 
the host, in UTM, you will need to manually sync up your assignment files. 

You can use `scp` to transmit files between your VM and Mac. For example, you 
edited the `server-c.c` file on your Mac and you want to test it inside the VM, 
run `scp -P2222 <path to server-c.c on your Mac> ubuntu@localhost:<path to server-c.c on your VM>` 
to transmit the file, then run the test script inside the VM.
