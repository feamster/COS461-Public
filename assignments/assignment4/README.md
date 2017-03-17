# Assignment 4: Passive Network Measurement

#### Due April 3 at 5:00pm

You may work with a partner on this assignment.

### Getting Started

On your host machine (not the VM), go to the course assignments directory:

```
$ cd COS461-Public/assignments
```
 Pull the latest update from Github.
```
$ git pull
```

Reprovision your VM to install necessary packages for this assignment.

```
$ vagrant reload --provision
```

Still on your host machine, open up your browser and type `localhost:8888` in the address bar. This should open to the Jupyter notebook file selection window.  Juypter notebook is actually running on port 8888 on your vagrant VM, but you can access it through your host machine browser because the port is being forwarded between the VM and the host machine.  

In the file selection window, enter the `assignment4` directory and then open `Assignment4_Notebook.ipynb`. This will open a notebook with the instructions for the rest of the assignment.  Work through this notebook from top to bottom and complete the sections marked "TODO."  

**Remember to "Save and Checkpoint" (from the "File" menu) before you leave the notebook or close your tab.**

### Jupyter Notebook

Jupyter Notebook (formerly called iPython Notebook) is a browser-based IDE with a cell-based editor.

Every cell in a notebook can contain either code or text. Begin editing a cell by double-clicking it. You can execute the code in a cell (or typeset the text) by pressing `shift-enter` with the cell selected.  Global variables and functions are retained across cells. Save your work with the "Save and Checkpoint" option in the "File" menu. If your code hangs, you can interrupt it with the "Interrupt" option in the "Kernel" menu.  You can also clear all variables and reset the environment with the "Restart" option in the "Kernel" menu.

The "Help" menu contains many additional resources about Jupyter notebooks (including a user interface tour, useful keyboard shortcuts, and links to tutorials).

### Submission
Submit your completed `Assignment4_Notebook.ipynb` file on CS Dropbox here: https://dropbox.cs.princeton.edu/COS461_S2017/Assignment_4_-_Passive_Network_Measurement. Submit only once for both partners. Remember to put your names and netids in the marked location at the top of the file.
