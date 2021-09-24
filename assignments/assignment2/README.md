# Assignment 2: TCP Congestion Control and Bufferbloat

### Due Friday October 8 at 11:59 pm EST

This is not a group assignment. You are not allowed to copy or look at code
from other students. However, you are welcome to discuss the assignments with
other students without sharing code.

## Getting Started

### For VirtualBox users

On your host machine (not the VM), go to the course assignments directory:

```
$ cd COS461-Public/assignments
```
 Pull the latest update from Github.
```
$ git pull
```

It is not necessary to reprovision your VM. You can just `vagrant ssh` into 
your VM if it's already provisioned. However, if you see that the Vagrantfile 
is updated when git pulling, you will need to reprovision your VM to install 
packages for this assignment, as below:
```
$ vagrant reload --provision
```

### (For Apple Silicon users)

`ssh` into your UTM VM, pull the latest update from Github:
```
$ git pull
```

If you see that the `setup.sh` file is updated, you can either apply the diff 
manually or delete your current VM (make sure your progress is backed up on 
your host machine) and follow the setup process in assignment1 README to 
reflect the changes. If not updated, nothing needs to be done for your VM.

## Starting up the Jupyter Notebook Server

In the VM, run the command `sudo jupyter notebook &`. This will
start a new Jupyter notebook server in the background. Even though it is
running in the background, it will sometimes print informative messages to the
terminal. You can press Enter each time you get a message to get the shell
prompt back. To shut down the notebook, run `fg` then press Control-C twice
(once to get the confirmation message, another time to skip confirmation).

While the notebook is running, on your host machine, open up your browser and
type `localhost:8888` in the address bar. This should take you to the Jupyter
notebook file selection window.  Juypter notebook is actually running on port
8888 on your vagrant VM, but you can access it through your host machine
browser because the port is being forwarded between the VM and the host
machine.  

In the file selection window, enter the `assignment2` directory and then open
`Assignment2_Notebook.ipynb`. This will open a notebook with the instructions
for the rest of the assignment.  Work through this notebook from top to bottom
and complete the sections marked "TODO."

**Remember to "Save and Checkpoint" (from the "File" menu) before you leave the
notebook or close your tab.**  

## Jupyter Notebook

Jupyter Notebook (formerly called iPython Notebook) is a browser-based IDE with
a cell-based editor.

Every cell in a notebook can contain either code or text ("Markdown"). Begin
editing a cell by double-clicking it. You can execute the code in a cell (or
typeset the text) by pressing `shift-enter` with the cell selected.  Global
variables and functions are retained across cells. Save your work with the
"Save and Checkpoint" option in the "File" menu. If your code hangs, you can
interrupt it with the "Interrupt" option in the "Kernel" menu.  You can also
clear all variables and reset the environment with the "Restart" option in the
"Kernel" menu.

The "Help" menu contains many additional resources about Jupyter notebooks
(including a user interface tour, useful keyboard shortcuts, and links to
tutorials).

## Submission

Submit your completed `Assignment2_Notebook.ipynb` file on TigerFile here: 
[Programming Assignment 2](https://tigerfile.cs.princeton.edu/COS461_F2021/Programming_Assignment_2).

Remember to put your name and netid in the marked location at the top of the
file.
#### Acknowledgement
This assignment is modeled after a [similar assignment](http://web.stanford.edu/class/cs244/pa1.html) at Stanford University.
