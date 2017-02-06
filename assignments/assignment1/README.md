# Assignment 1: Virtual Machine Setup & Socket Programming

##### Due Monday Februrary 20 at 5:00 pm

Welcome to COS 461: Computer Networks! Through this and the following  assignments, you will gain hands-on experience with real-world network programming.  You will write a program that allows your computer to communicate with another, be it across the room or across the world. You will program a router to deliver information to the right destination in a network with thousands of nodes.  You will learn how decisions made by protocol designers and network administrators affect Internet performance.  You will analyze data from Princeton's own network to detect security threats and learn how to prevent them.

The programming assignments are designed to be challenging but manageable in the time allotted. If you have questions, want to suggest clarifications, or are struggling with any of the assignments this semester, please come to office hours, ask questions on Piazza, or talk to an instructor before or after class.

You are not allowed to copy or look at code from other students. However, you are welcome to discuss the assignments with other students without sharing code.

Let's get started!

## Part A: Set Up Virtual Machine
The first part of this assignment is to set up the virtual machine (VM) you will use for the rest of the course. This will make it easy to install all dependencies for the programming assignments, saving you the tedium of installing individual packages and ensuring your development environment is correct.

##### Step 1: Install Vagrant
Vagrant is a tool for automatically configuring a VM using instructions given in a single "Vagrantfile."  You need to install Vagrant using the correct download link for your computer here: https://www.vagrantup.com/downloads.html.

##### Step 2: Install VirtualBox
VirtualBox is a VM provider (hypervisor). You need to install VirtualBox using the correct download link for your computer here: https://www.virtualbox.org/wiki/Downloads. The links are under the heading "VirtualBox 5.1.14 platform packages."

##### Step 3: Install Git
Git is a distributed version control system.  You need to install Git using the correct download link for your computer here: https://git-scm.com/downloads.

##### Step 4: Install X Server and SSH-capable terminal
You will need SSH and X Server to input commands to the virtual machine.  
 * For Windows, install [Xming](https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/Xming-6-9-0-31-setup.exe/download) and [PuTTY](http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe)
 * For macOS, install [XQuartz](https://www.xquartz.org/) (Terminal is pre-installed)
 * for Linux, both X server and SSH capable terminal are pre-installed.

##### Step 5: Clone course Git repository
Open your terminal and `cd` to wherever you want to keep files for this course on your computer.  

Run `git clone https://github.com/PrincetonUniversity/COS461-Public` to download the course files from GitHub

`cd COS461-Public/assignments` to enter the course assignment directory

##### Step 6: Provision virtual machine using Vagrant
Run the command  `vagrant up` to start the VM and  provision it according to the Vagrantfile.

**Note**: The following commands will allow you to stop the VM at any point (such as when you are done working on an assignment for the day):
* `vagrant suspend` will save the state of the VM and stop it.
* `vagrant halt` will gracefully shutdown the VM operating system and power down the VM.
* `vagrant destroy` will remove all traces of the VM from your system. If you have important files saved on the VM (like your assignment solutions) **DO NOT** use this command.

##### Step 7: Test SSH to VPN

Run `vagrant ssh` from your terminal. This is the command you will use every time you want to access the VM. If it works, your terminal prompt will change to `vagrant@cos461:~$`. All further commands will execute on the VM. You can then run `cd /vagrant` to get to the course directory that's shared between your regular OS and the VM.

Vagrant is especially useful because of this shared directory structure.  You don't need to copy files to and from the VM. Any file or directory in the `assignments` directory where the `Vagrantfile` is located is automatically shared between your computer and the virtual machine.

The command `logout` will stop the SSH connection at any point.

##### Step 8: Go take a break. You've earned it!

## Part B: Socket Programming

As discussed in lecture, socket programming is the standard way to write programs that communicate over a network. While originally developed for Unix computers programmed in C, the socket abstraction is general and not tied to any specific operating system or programming language. This allows programmers to use the socket mental model to write correct network programs in many contexts.

This part of the assignment will give you experience with basic socket programming.  You will write 2 pairs of TCP client and server programs for sending and receiving text messages over the Internet. One client/server pair must be written in C. The other pair can be written in **either** Python or Go. You can choose either language. The Python solution is shorter, but you will need to know Go socket programming for a later assignment.

The client and server programs in both languages should meet the following specifications. Be sure to read these before and after programming to make sure your implementation fulfills them:

##### Server specification
* Each server program should listen on a socket, wait for a client to connect, receive a message from the client, print the message to stdout, and then wait for the next client indefinitely.
* Each server should take one command-line argument: the port number to listen on for client connections.
* Each server should accept and process client communications in an infinite loop, allowing multiple clients to send messages to the same server. The server should only exit in response to an external signal (e.g. SIGINT from pressing `ctrl-c`).
* Each server should maintain a short (5-10) client queue and handle multiple client connection attempts sequentially. In real applications, a TCP server would fork a new process to handle each client connection concurrently, but that is not necessary for this assignment.
* Each server should gracefully handle error values potentially returned by socket programming library functions (see specifics for each language below).

##### Client specification
* Each client program should contact a server, read a message from stdin, send the message, and exit.
* Each client should read and send the message *exactly* as it appears in stdin until reaching an EOF (end-of-file).
* Each client should take two command-line arguments: the IP address of the server and the port number of the server.
* Each client must be able to handle arbitrarily large messages by iteratively reading and sending chunks of the message, rather than reading the whole message into memory first.
* Each client should handle partial sends (when a socket only transmits part of the data given in the last `send` call) by attempting to re-send the rest of the data until it has all been sent.
* Each client should gracefully handle error values potentially returned by socket programming library functions.

##### Getting started

Do all programming and testing on the Vagrant VM. Both Emacs and Vim text editors are pre-installed. After running `vagrant ssh` from your terminal, run `cd /vagrant` to get to the course directory.

We have provided scaffolding code in the `assignment1/client_server/` directory.
*You should read and understand this code before starting to program.*

You should program only in the locations of the provided files marked with `TODO` comments. There is one `TODO` section per client and one per server. You can add functions if you wish, but do not change file names, as they will be used for automated testing.

The following sections provide details for the client and server programs in each language.

##### C
The classic "Beej's Guide to Network Programming" is located here: http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html.  The [system call section](http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html#syscalls) and [client/server example section](http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html#clientserver) will be most relevant. The man pages are also useful for looking up individual functions (e.g.  `man socket`).

The files `client-c.c` and `server-c.c` contain scaffolding code. You will need to add socket programming and I/O code in the locations marked `TODO`. The reference solutions have roughly 70  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

You should build your solution by running `make` in the `assignment1/client_server` directory. Your code *must* build using the provided Makefile. The server should be run as `./server-c [port] > [output file]`. The client should be run as `./client-c [server IP] [server port] < [message file]`.

##### Python
The documentation for Python socket programming is located here: https://docs.python.org/2/library/socket.html.  The first few paragraphs at the top, the [section on socket objects](https://docs.python.org/2/library/socket.html#socket-objects) and the [first example](https://docs.python.org/2/library/socket.html#example) are particularly relevant.

The files `client-python.py` and `server-python.py` contain the scaffolding code. You will need to add socket programming code in the locations marked `TODO`. The reference solutions have roughly 15  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

The Python socket functions will automatically raise Exceptions with helpful error messages. No additional error handling is required.

The server should be run as `python server-python.py [port] > [output file]`. The client should be run as `python client-python.py [server IP] [server port] < [message file]`.

##### Go
The documentation for Go socket programming is located here: https://golang.org/pkg/net/.  The overview at the top and the  section on the [Conn type](https://golang.org/pkg/net/#Conn) will be most relevant.

The files `client-go.go` and `server-go.go` contain the scaffolding code. You will need to add socket programming code in the locations marked `TODO`. The reference solutions have roughly 40  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

The Go `Listen` function maintains a queue of connecting clients by default. No additional programming is required.

You should build your solution by running `make go` in the `assignment1/client_server` directory. Your code *must* build using the provided Makefile. The server should be run as `./server-go[port] > [output file]`. The client should be run as `./client-go [server IP] [server port] < [message file]`.

##### Testing

You should test your implementations by attempting to send messages from your clients to your servers. The server can be run in the background (append a `&` to the command) or in a separate SSH window. You should use `127.0.0.1` as the server IP and a high server port number between 10000 and 60000. You can kill a background server with the command `fg` to bring it to the foreground then `ctrl-c`.

The Bash script `test_client_server.sh` will test your implementation by attempting to send the same message ("Go Tigers!\n") between all 4 combinations of your clients and servers (C client to C server, C client to Python/Go server, etc.). Run the script as

`./test_client_server.sh [python|go] [server port]`

If you get a permissions error, run `chmod 744 test_client_server.sh` to give the script execute privileges.

For each client/server pair, the test script will print "SUCCESS" if the message is sent and received correctly. Otherwise it will print a diff of the sent and received message.

###### Debugging hints
Here are some debugging tips. If you are still having trouble, ask a question on Piazza or see an instructor during office hours.

* There are defined buffer size and queue length constants in the scaffolding code. Use them. If they are not defined in a particular file, you don't need them.
* There are multiple ways to read and write from stdin/stdout in C, Python, and Go. Any method is acceptable as long as it does not read an unbounded amount into memory at once and does not modify the message.
* If you are using buffered I/O to write to stdout, make sure to call `flush` or the end of a long message may not write.
* Remember to close the socket at the end of the client program.
* Make sure you are using `127.0.0.1` as the server IP argument to the client and the same server port for both client and server programs.
* If you get "address already in use" errors, make sure you don't already have a server running. Otherwise, restart your ssh session.  
* If you are getting other connection errors, try a different port between 10000 and 60000.

##### Submission and grading
Submit the assignment by uploading your modified client and server files to CS DropBox here: https://dropbox.cs.princeton.edu/COS461_S2017/Assignment_1_-_Socket_Programming.

We will grade your assignments by running the `test_client_server.sh` script and additional tests with large messages, multiple simultaneous clients, etc. Double check the specifications above and perform your own tests before submitting.
