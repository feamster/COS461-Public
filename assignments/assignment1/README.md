# Assignment 1: Virtual Machine Setup & Socket Programming

### Due Monday February 18 at 5:00 pm

Welcome to COS 461: Computer Networks! Through this and the following  assignments, you will gain hands-on experience with real-world network programming.  You will write a program that allows your computer to communicate with another, be it across the room or across the world. You will program a router to deliver information to the right destination in a network with thousands of nodes.  You will learn how decisions made by protocol designers and network administrators affect Internet performance.  You will analyze data from Princeton's own network to detect security threats and learn how to prevent them.

The programming assignments are designed to be challenging but manageable in the time allotted. If you have questions, want to suggest clarifications, or are struggling with any of the assignments this semester, please come to office hours, ask questions on Piazza, or talk to an instructor before or after class.

You are not allowed to copy or look at code from other students. However, you are welcome to discuss the assignments with other students without sharing code.

Let's get started!

## Part A: Set Up Virtual Machine
The first part of this assignment is to set up the virtual machine (VM) you will use for the rest of the course. This will make it easy to install all dependencies for the programming assignments, saving you the tedium of installing individual packages and ensuring your development environment is correct.

### Step 1: Install Vagrant
Vagrant is a tool for automatically configuring a VM using instructions given in a single "Vagrantfile."

**macOS & Windows:** You need to install Vagrant using the correct download link for your computer here: https://www.vagrantup.com/downloads.html.

**Windows only**: You will be asked to restart your computer at the end of the installation. Click Yes to do so right away, or restart manually later,
but don't forget to do so or Vagrant will not work!

**Linux:** First, make sure your package installer is up to date by running the command `sudo apt-get update`. To install Vagrant, you must have the "Universe" repository on your computer; run `sudo apt-add-repository universe` to add it. Finally, run `sudo apt-get install vagrant` to install vagrant.

### Step 2: Install VirtualBox
VirtualBox is a VM provider (hypervisor).

**macOS & Windows:** You need to install VirtualBox using the correct download link for your computer here: https://www.virtualbox.org/wiki/Downloads. The links are under the heading "VirtualBox 5.x.x platform packages."

**Windows only:** Use all the default installation settings, but you can uncheck the "Start Oracle VirtualBox 5.x.x after installation" checkbox.

**Linux:** Run the command `sudo apt-get install virtualbox`.

**Note:** This will also install the VirtualBox application on your computer, but you should never need to run it, though it may be helpful (see Step 6).

### Step 3: Install Git (and SSH-capable terminal on Windows) 
Git is a distributed version control system.

**macOS & Windows:** You need to install Git using the correct download link for your computer here: https://git-scm.com/downloads.

**macOS only:** Once you have opened the .dmg installation file, you will see a Finder window including a .pkg file, which is the installer. Opening this normally may give you a prompt saying it can't be opened because it is from an unidentified developer. To override this protection, instead right-click on thet .pkg file and select "Open". This will show a prompt asking you if you are sure you want to open it. Select "Yes". This will take you to the (straightforward) installation.

**Windows only:** You will be given many options to choose from during the installation; using all the defaults will be sufficient for this course (you can uncheck "View release notes" at the end). The installation includes an SSH-capable Bash terminal usually located at `C:\Program Files\Git\bin\bash.exe`. You should use this as your terminal in this class, unless you prefer another SSH-capable terminal (the command prompt will not work). Feel free to create a shortcut to it; copying and pasting the executable somewhere else will not work, however.

**Linux:** `sudo apt-get install git`.

### Step 4: Install X Server
You will need an X Server to input commands to the virtual machine.

**macOS:** Install [XQuartz](https://www.xquartz.org/). You will need to log out and log back in to complete the installation (as mentioned by the prompt at the end).

**Windows:** Install [Xming](https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/Xming-6-9-0-31-setup.exe/download). Use default options and uncheck "Launch Xming" at the end.

**Linux:** The X server is pre-installed!

### Step 5: Clone course Git repository
Open your terminal (use the one mentioned in step 3 if using Windows) and `cd` to wherever you want to keep files for this course on your computer.  

Run `git clone https://github.com/PrincetonUniversity/COS461-Public` to download the course files from GitHub.

`cd COS461-Public/assignments` to enter the course assignment directory.

### Step 6: Provision virtual machine using Vagrant
From the `assignments` directory you just entered, run the command  `vagrant up` to start the VM and  provision it according to the Vagrantfile. You will likely have to wait several minutes. You may see warnings/errors in red, such as "default: stdin: is not a tty", but you shouldn't have worry about them.

**Note 1**: The following commands will allow you to stop the VM at any point (such as when you are done working on an assignment for the day):
* `vagrant suspend` will save the state of the VM and stop it.
* `vagrant halt` will gracefully shutdown the VM operating system and power down the VM.
* `vagrant destroy` will remove all traces of the VM from your system. If you have important files saved on the VM (like your assignment solutions) **DO NOT** use this command.

Additionally, the command `vagrant status` will allow you to check the status of your machine in case you are unsure (e.g. running, powered off, saved...).
You must be in some subdirectory of the directory containing the Vagrantfile to use any of the commands above, otherwise Vagrant will not know which VM you are referring to.

**Note 2**: The VirtualBox application that was installed in Step 2 provides a visual interface as an alternative to these commands, where you can see the status of your VM and power it on/off or save its state. It is not recommended to use it, however, since it is not integrated with Vagrant, and typing commands should be no slower. It is also not an alternative to the initial `vagrant up` since this creates the VM.

### Step 7: Test SSH to VPN

Run `vagrant ssh` from your terminal. This is the command you will use every time you want to access the VM. If it works, your terminal prompt will change to `vagrant@cos461:~$`. All further commands will execute on the VM. You can then run `cd /vagrant` to get to the course directory that's shared between your regular OS and the VM.

Vagrant is especially useful because of this shared directory structure.  You don't need to copy files to and from the VM. Any file or directory in the `assignments` directory where the `Vagrantfile` is located is automatically shared between your computer and the virtual machine. This means you can use your IDE of choice from outside the VM to write your code (but will still have to build and run within the VM).

The command `logout` will stop the SSH connection at any point.

### Extra Note for Windows users

Line endings are symbolized differently in DOS (Windows) and Unix (Linux/MacOS). In the former, they are represented by a carriage return and line feed (CRLF, or "\r\n"), and in the latter, just a line feed (LF, or "\n"). Given that you ran `git pull` from Windows, git detects your operating system and adds carriage returns to files when downloading. This can lead to parsing problems within the VM, which runs Ubuntu (Unix). Fortunately, this only seems to affect the shell scripts (\*.sh files) we wrote for testing. The `Vagrantfile` is set to automically convert all files back to Unix format, so **you shouldn't have to worry about this**. **However**, if you want to write/edit shell scripts to help yourself with testing, or if you encounter this problem with some other type of file, use the preinstalled program `dos2unix`. Run `dos2unix [file]` to convert it to Unix format (before editing/running in VM), and run `unix2dos [file]` to convert it to DOS format (before editing on Windows). A good hint that you need to do this when running from the VM is some error message involving `^M` (carriage return). A good hint you need to do this when editing on Windows is the lack of new lines. Remember, doing this should only be necessary if you want to edit shell scripts.

### Step 8: Go take a break. You've earned it!

## Part B: Socket Programming

**Part B is individual.**

As discussed in lecture, socket programming is the standard way to write programs that communicate over a network. While originally developed for Unix computers programmed in C, the socket abstraction is general and not tied to any specific operating system or programming language. This allows programmers to use the socket mental model to write correct network programs in many contexts.

This part of the assignment will give you experience with basic socket programming.  You will write 2 pairs of TCP client and server programs for sending and receiving text messages over the Internet. One client/server pair must be written in C. The other pair can be written in **either** Python or Go. You can choose either language (only one). The Python solution is shorter, but you will need to know Go socket programming for a later assignment.

The client and server programs in both languages should meet the following specifications. Be sure to read these meticulously before and after programming to make sure your implementation fulfills them:

### Server specification
* Each server program should listen on a socket, wait for a client to connect, receive a message from the client, print the message to stdout, and then wait for the next client indefinitely.
* Each server should take one command-line argument: the port number to listen on for client connections.
* Each server should accept and process client communications in an infinite loop, allowing multiple clients to send messages to the same server. The server should only exit in response to an external signal (e.g. SIGINT from pressing `ctrl-c`).
* Each server should maintain a short (5-10) client queue and handle multiple client connection attempts sequentially. In real applications, a TCP server would fork a new process to handle each client connection concurrently, but that is **not necessary** for this assignment.
* Each server should gracefully handle error values potentially returned by socket programming library functions (see specifics for each language below). Errors related to handling client connections should not cause the server to exit after handling the error; all others should.

### Client specification
* Each client program should contact a server, read a message from stdin, send the message, and exit.
* Each client should read and send the message *exactly* as it appears in stdin until reaching an EOF (end-of-file).
* Each client should take two command-line arguments: the IP address of the server and the port number of the server.
* Each client must be able to handle arbitrarily large messages by iteratively reading and sending chunks of the message, rather than reading the whole message into memory first.
* Each client should handle partial sends (when a socket only transmits part of the data given in the last `send` call) by attempting to re-send the rest of the data until it has all been sent.
* Each client should gracefully handle error values potentially returned by socket programming library functions.

### Getting started

Do all building and testing on the Vagrant VM. You may either write your code on the Vagrant VM (both Emacs and Vim text editors are pre-installed) or directly on your OS (allowing you to use any editor you ahev installed). After running `vagrant ssh` from your terminal, run `cd /vagrant` to get to the course directory.

We have provided scaffolding code in the `assignment1/client_server/` directory.
*You should read and understand this code before starting to program.*

You should program only in the locations of the provided files marked with `TODO` comments. There is one `TODO` section per client and one per server. You can add functions if you wish, but do not change file names, as they will be used for automated testing.

The following sections provide details for the client and server programs in each language.

### C
The classic "Beej's Guide to Network Programming" is located here: https://beej.us/guide/bgnet/html/single/bgnet.html.
The [system call section](https://beej.us/guide/bgnet/html/single/bgnet.html#syscalls) and [client/server example section](https://beej.us/guide/bgnet/html/single/bgnet.html#clientserver) will be most relevant. The man pages are also useful for looking up individual functions (e.g. `man socket`).

The files `client-c.c` and `server-c.c` contain scaffolding code. You will need to add socket programming and I/O code in the locations marked `TODO`. The reference solutions have roughly 70  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

For error handling, you can call `perror` for socket programming functions that set the global variable `errno` (Beej's Guide will tell you which do). For those that don't, simply print a message to standard error.

You should build your solution by running `make` in the `assignment1/client_server` directory. Your code *must* build using the provided Makefile. The server should be run as `./server-c [port] > [output file]`. The client should be run as `./client-c [server IP] [server port] < [message file]`. See "Testing" for more details.

### Python
The documentation for Python socket programming is located here: https://docs.python.org/2/library/socket.html.  The first few paragraphs at the top, the [section on socket objects](https://docs.python.org/2/library/socket.html#socket-objects) and the [first example](https://docs.python.org/2/library/socket.html#example) are particularly relevant.

The files `client-python.py` and `server-python.py` contain the scaffolding code. You will need to add socket programming code in the locations marked `TODO`. The reference solutions have roughly 15  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

The Python socket functions will automatically raise Exceptions with helpful error messages. No additional error handling is required.

The server should be run as `python server-python.py [port] > [output file]`. The client should be run as `python client-python.py [server IP] [server port] < [message file]`. See "Testing" for more details.

### Go
The documentation for Go socket programming is located here: https://golang.org/pkg/net/.  The overview at the top and the  section on the [Conn type](https://golang.org/pkg/net/#Conn) will be most relevant.

The files `client-go.go` and `server-go.go` contain the scaffolding code. You will need to add socket programming code in the locations marked `TODO`. The reference solutions have roughly 40  (well commented and spaced) lines of code in the `TODO` sections of each file. Your implementations may be shorter or longer.

The Go `Listen` function maintains a queue of connecting clients by default. No additional programming is required.

You should build your solution by running `make go` in the `assignment1/client_server` directory. Your code *must* build using the provided Makefile. The server should be run as `./server-go [port] > [output file]`. The client should be run as `./client-go [server IP] [server port] < [message file]`. See "Testing" for more details.

### Testing

You should test your implementations by attempting to send messages from your clients to your servers. The server can be run in the background (append a `&` to the command) or in a separate SSH window. You should use `127.0.0.1` as the server IP and a high server port number between 10000 and 60000. You can kill a background server with the command `fg` to bring it to the foreground then `ctrl-c`.

The Bash script `test_client_server.sh` will test your implementation by attempting to send several different messages between all 4 combinations of your clients and servers (C client to C server, C client to Python/Go server, etc.). The messages are the following:

0. The short message "Go Tigers!\n"
0. A long, randomly generated alphanumeric message
0. A long, randomly generated binary message
0. Several short messages sent sequentially from separate clients to one server
0. Several long, random alphaumeric messages sent concurrently from separate clients to one server

Run the script as

`./test_client_server.sh [python|go] [server port]`

If you get a permissions error, run `chmod 744 test_client_server.sh` to give the script execute privileges.

For each client/server pair, the test script will print "SUCCESS" if the message is sent and received correctly. Otherwise it will print a diff of the sent and received message if the diff output is human-readable, i.e., just for tests 1 and 4.

### Debugging hints
Here are some debugging tips. If you are still having trouble, ask a question on Piazza or see an instructor during office hours.

* There are defined buffer size and queue length constants in the scaffolding code. Use them. If they are not defined in a particular file, you don't need them. If you are not using one of them, either you have hard-coded a value, which is bad style, or you are very likely doing something wrong.
* There are multiple ways to read and write from stdin/stdout in C, Python, and Go. Any method is acceptable as long as it does not read an unbounded amount into memory at once and does not modify the message.
* If you are using buffered I/O to write to stdout, make sure to call `flush` or the end of a long message may not write.
* Remember to close the socket at the end of the client program.
* When testing, make sure you are using `127.0.0.1` as the server IP argument to the client and the same server port for both client and server programs.
* If you get "address already in use" errors, make sure you don't already have a server running. Otherwise, restart your ssh session with the command `logout` followed by `vagrant ssh`.  
* If you are getting other connection errors, try a different port between 10000 and 60000.

### Q&A
* **I'm getting an error when I run the command `vagrant up`. What do I do?** Many errors/warnings are not a problem and do not need to be addressed, such as `==> default: stdin: is not a tty`. Usually, errors starting with `==> default` should not be worried about, but others should, in particular if they cause the process to be aborted. Use `vagrant status` to see if the VM is running after `vagrant up`; if it is not, then there is a real problem. Here are some known errors and how to fix them:
    * **"A Vagrant environment or target machine is required to run this command..."**: you must run `vagrant up` from a subdirectory of the directory containing the Vagrantfile (in the case, `assignments`).
    * **"Vagrant cannot forward the specified ports on this VM, since they would collide with some other application that is already listening on these ports..."**: perhaps you cloned the repository twice and the VM is already running on one of them. Since they both use the same port, they cannot run at the same time. You may also have some other application using port 8888. To help find what is using it, follow [these](http://osxdaily.com/2014/05/20/port-scanner-mac-network-utility/) instructions for macOS, [these](https://techtalk.gfi.com/scan-open-ports-in-windows-a-quick-guide/) for Windows and [these](https://wiki.archlinux.org/index.php/Nmap#Port_scan) for Linux (you may have to install `nmap`). Use 127.0.0.1 as the IP and 8888-8888 as the port range in your port scan.

  If this did not help you fix the problem, please ask on Piazza or at office hours. 

* **Should I set the `MSG_WAITALL` flag on `recv()`?** No. This causes `recv()` to not return until it receives a specified amount of data. However, the server cannot know this amount in advance, so you should instead keep calling `recv()` until there is nothing left to receive.
* **Do I need to handle signals such as SIGINT to clean up the server process when the user presses `ctrl-c`?** No, it is not necessary in this assignment. The default response to signals is good enough. Keep in mind it would be good practice to do so in general, however.
* **Should I use stream or datagram sockets?** Please use stream sockets, to ensure that the exact message is delivered. Datagram packets are not guaranteed to be delivered.
* **Should the client wait to receive a reply from the server?** No, in this assignment it should exit immediately after sending all the data.
* **Should the server handle client connections concurrently (in seperate processes)?** No, as stated in the client specification, this is not required in this assignment. So no need to use `fork()`!


### Submission and grading
Submit the assignment by uploading your modified client and server files to CS DropBox here: [Assignment 1 - Socket Programming](https://dropbox.cs.princeton.edu/COS461_S2019/Assignment-1-Socket-Programming).

We will grade your assignments by running the `test_client_server.sh` script and additional tests with large messages, multiple simultaneous clients, etc. Double check the specifications above and perform your own tests before submitting.

Code that does not compile is graded harshly; if you want partial credit on code that doesn't compile, comment it out and make sure your file compiles!

Remember that, in addition to your C client/server pair, you should submit another client/server in **either** Python or Go, but not both! If you submit both pairs we will only grade your Python files (arbitrary choice). Do not expect us to grade both and select the greater of the two grades. Furthermore, you may NOT submit just a client in Python and a server in Go, or the other way around. Your second client/server pair must be in the same language.
