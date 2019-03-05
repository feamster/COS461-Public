# Assignment 2: Intradomain Routing Algorithms

### Due March 4th, 5:00pm

The Internet is composed of many independent networks (called autonomous systems) that must cooperate in order for packets to reach their destinations.  This necessitates different protocols and algorithms for routing packet within autonomous systems, where all routers are operated by the same entity, and between autonomous systems, where business agreements and other policy considerations affect routing decisions.

This assignment focuses on intradomain routing algorithms used by routers within a single autonomous system (AS). The goal of intradomain routing is typically to forward packets along the shortest or lowest cost path through the network.

The need to rapidly handle unexpected router or link failures, changing link costs (usually depending on traffic volume), and connections from new routers and clients, motivates the use of distributed algorithms for intradomain routing.  In these distributed algorithms, routers start with only their local state and must communicate with each other to learn lowest cost paths.

Nearly all intradomain routing algorithms used in real-world networks fall into one of two categories, distance-vector or link-state.  In this assignment, you will implement distributed  distance-vector and link-state routing algorithms in Python and test them with a provided network simulator.

**You should work with a partner.** The Piazza "search for teammates" feature is active for this assignment. See "Submission and Grading" below for partner submission details.  

## Background Reading
Begin by reading pages 240-258 in the textbook *Computer Networks: A Systems Approach* (5th edition) by Peterson & Davie.  An excerpt of these pages is included in the `assignment2` directory with the filename `textbook_reading.pdf`. There is also a copy of the textbook in the Friend library.

This reading provides enough information to design both the distance-vector and link-state routing algorithms. Be sure you understand how both algorithms work before starting to code. The box at the bottom of page 258 summarizes the difference between the two algorithms (reprinted here):

  "In distance-vector, each node talks only to its directly connected neighbors, but it tells them everything it has learned (i.e. distance to all nodes).  In link-state, each node talks to all other nodes, but it tells them only what it knows for sure (i.e. only the state of its directly connected links)."

## Provided code

### Download
Open your terminal and `cd` into the `<>/assignments` directory you downloaded in Assignment 1. Run the command `git pull` to download the code for this assignment.

Run `vagrant reload --provision` to install the needed libraries for this assignment and start the VM (no need to run `vagrant up` in addition).

Then run `vagrant ssh` and `cd /vagrant` to enter the virtual machine just as you did in Assignment 1.  The provided code is located in the `/vagrant/assignments/assignment2` directory of your vagrant VM.

### Familiarize yourself with the network simulator
The provided code implements a network simulator that abstracts away many details of a real network, allowing you to focus on intradomain routing algorithms.  Each `.json` file in the `assignment2` directory is the specification for a different network simulation with different numbers of routers, links, and link costs. Some of these simulations also contain link additions and/or failures that will occur at pre-specified times.  

The network simulator can be run with or without a graphical interface. For example, the command `python visualize_network.py 01_small_net.json` will run the simulator on a simple network with 2 routers and 3 clients. The default router implementation returns all traffic back out the link on which it arrives. This is obviously a terrible routing algorithm, which your implementations will fix.

The network architecture is shown on the left side of the visualization. Routers are colored red, clients are colored blue. Each client periodically sends gray traceroute-like packets addressed to every other client in the network. These packets remember the sequence of routers they traverse, and the most recent route taken to each client is printed in the text box on the top right. This is an important debugging tool.

The cost of each link is printed on the connections.

Clicking on a client hides all packets except those addressed to that client, so you can see the path chosen by the routers. Clicking on the client again will go back to showing all packets.

Clicking on a router causes a string about that router to print in the text box on the lower right. You will be able to set the contents of this string for debugging your router implementations.

The same network simulation can be run without the graphical interface by the command `python network.py 01_small_net.json`. The simulation will run faster without having to go at visualizable speed. It will stop after a predetermined amount of time, print the final routes taken by the traceroute packets to and from all clients and whether these routes are correct given the known lowest-cost paths through the network.

## Implementation instructions

Your job is to complete the `DVrouter` and `LSrouter` classes in the `DVrouter.py` and `LSrouter.py` files so they implement distance-vector or link-state routing algorithms, respectively.

The simulator will run independent instances of your completed `DVrouter` or `LSrouter` classes in separate threads, simulating independent routers in a network.

You will notice that the `DVrouter` and `LSrouter` classes contain several unfinished methods marked with `TODO` (including `handlePacket`, `debugString`, etc.). These methods override those in the `Router` superclass (in `router.py`) and are called by the simulator when a corresponding event occurs (e.g. `handlePacket()` will be called when a router instance receives a packet).

The arguments to these methods contain all the information you need to implement the routing algorithms. Each of these methods is described in greater detail below.  

In addition to completing each of these methods, you are free to add additional fields (instance variables) or helper methods to the `DVrouter` and `LSrouter` classes.

**Use the descriptions in `textbook_reading.pdf` to design your solutions.** You will be graded on whether your solutions find lowest cost paths in the face of link failures and additions. Here are a few further simplifications:
* Each client and router in the network simulation has a single static address. Do not worry about address prefixes, families, or masks

* You do not need to worry about packet authentication and checksums. Assume that a lower layer protocol handles corruption checking

* As long your routers behave correctly when notified of link additions and failures, you do not need to worry about time-to-live (TTL) fields. The network simulations are short and routers/links will not fail silently.

* There is an example implementation of distance-vector routing on textbook pages 249-250. It is in C, so you can't copy it directly, but definitely use it to inform your implementation

* Page 248 discusses the "count-to-infinity" problem for distance-vector routing.  You will need to handle this problem, but you can choose the small infinity solution (infinity = 16 is fine for the networks in this assignment), split horizon, or split horizon with   poison reverse.  

* Link-state routing involves reliably flooding link state updates.  You will need the sequence number component of this protocol, but you will not need to check (via acknowledgements and retransmissions) that LSPs send successfully between adjacent routers. Assume that a lower-level protocol makes single-hop sends reliable.

* Finally, LS and DV routing involve periodically sending routing information even if no detected change has occurred. This allows changes occurring far away in the network to propagate even if some routers do not change their routing tables in response to these changes (important for this assignment). It also allows detection of silent router failures (not tested in this assignment).  You implementations should send periodic routing packets every `heartbeatTime` milliseconds where `heartbeatTime` is an argument to the `DVrouter` or `LSrouter` constructor.  You will regularly get the current time in milliseconds as an argument to the `handleTime` method (see below).

### Restrictions
There are limitations on what information your `DVrouter` and `LSrouter` classes are allowed to access from the other provided Python files. Unlike C and Java, Python does not support private variables and classes.  Instead, the list of limitations here will be checked when grading.  Violating any of these requirements will result in serious grade penalties.

* Your solution must not require modification to any files other than  `DVrouter.py` and `LSrouter.py`. The grading tests will be performed with unchanged versions of the other files.


* Your code may not call any functions or methods, instantiate any classes, or access any variables defined in any of the other provided python files, with the following exceptions:
  * `LSrouter` and `DVrouter` can call the inherited `send` function of the `Router` superclass (e.g. `self.send(port, packet)`).
  * `LSrouter` and `DVrouter` can access the `addr` field of the `Router` superclass (e.g. `self.addr`) to get their own address.
  * `LSrouter` and `DVrouter` can create new `Packet` objects and call any of the methods defined in `packet.py` *EXCEPT* for `getRoute()`, `addToRoute()`, and `animateSend()`. You can access and change any of the fields of a `Packet` object EXCEPT for `route`. 


### Method descriptions
These are the methods you need to complete in `DVrouter` and `LSrouter`:

* `__init__(self, addr, heartbeatTime)`
  * Class constructor. `addr` is the address of this router.  Add your own class fields and initialization code (e.g. to create routing table and/or forwarding table data structures). Routing information should be sent by this router at least once every `heartbeatTime` milliseconds.


* `handlePacket(self, port, packet)`
  * Process incoming packet: This method is called whenever a packet arrives at the router on port number `port`. You should check whether the packet is a traceroute packet or a routing packet and handle it appropriately. Methods and fields of the packet class are defined in `packet.py`.


* `handleNewLink(self, port, endpoint, cost)`
  * This method is called whenever a new link is added to the router on port number `port` connecting to a router or client with address `endpoint` and link cost `cost`.  You should store the argument values in a data structure to use for routing. If you want to send packets along this link, call `self.send(port, packet)`.  


* `handleRemoveLink(self, port)`
  * This method is called when the existing link on port number `port` is disconnected. You should update data structures appropriately.


* `handleTime(self, timeMillisecs)`
  * This method is called regularly and provides you with the current time in millisecs for sending routing packets at regular intervals.


* `debugString(self)`
  * This method is called by the network visualization to print current details about the router.  It should return any string that will be helpful for debugging. This method is for your own use and will not be graded.

### Creating and sending packets
You will need to create packets to send information between routers using the `Packet` class defined in `packet.py`. Any packet `p` you create to send routing information should have `p.kind == ROUTING`.

You will have to decide what to include in the `content` field of these packets. The content should be reasonable for the algorithm you are implementing (e.g. don't send an entire routing table for link-state routing).  

Packet content must be a string. This is checked by an assert statement when the packet is sent. `DVrouter` and `LSrouter` import the `dumps()` and `loads()` functions which return a string (in json format) when given a python object. Using these functions is an easy way to stringify and de-stringify.

You can access and set/modify any of the fields of a packet object (including `content`, `srcAddr`, `dstAdddr` and `kind`) except for `route` (see "Restrictions" above).

### Link reliability
If a link between two routers fails or is added, the appropriate `handle` function will *always* be called on both routers after the failure or addition.

Links have varying latencies (usually proportional to their costs). Packets may not arrive in the global order that they are sent.

### Ceci n'est pas un network...
The simulated network in this assignment abstracts away many details you would need to consider when implementing distance-vector or link-state algorithms on real routers.  This should allow you to focus on the core ideas of the algorithms without worrying about other protocols (e.g. ARP) or meticulous systems programming issues.  If you are curious about these real-world details, please ask on Piazza or in office hours.

## Running and Testing
You should test your `DVrouter` and `LSrouter` using the provided network simulator.  There are multiple json files defining different network architectures and  link failures and additions.  "05_pg242_net.json" and "03_pg244_net.json" files define the networks on pages 242 and 244 of the provided textbook reading respectively.  The json files without "events" in their file name do not have link failures or additions and are good for initial testing.

Run the simulation with the graphical interface using the command

`python visualize_network.py [networkSimulationFile.json] [DV|LS]`

The argument `DV` or `LS` indicates whether to run `DVrouter` or `LSrouter`, respectively.  

Run the simulation without the graphical interface with the command

`python network.py [networkSimulationFile.json] [DV|LS]`

The routes to and from each client at the end of the simulation will print, along with whether they match the reference lowest-cost routes. If the routes match, your implementation has passed for that simulation.  If they do not, continue debugging (using print statements and the `debugString()` method in your router classes).

The bash script `test_dv_ls.sh` will run all the supplied networks with your router implementations. You may need to run `chmod 744 test_dv_ls.sh` first to make the script executable.  You can also pass "LS" or "DV" as an argument to `test_dv_ls.sh` (e.g. `test_dv_ls.sh DV`) to test only one implementation.

Don't worry if you get the following error. It sometimes occurs when the threads are stopped at the end of the simulation without warning:

```
Unhandled exception in thread started by
sys.excepthook is missing
lost sys.stderr
```

## Submission and Grading

Only one partner should submit the `DVrouter.py` and `LSrouter.py` files to the CS Dropbox here: https://dropbox.cs.princeton.edu/COS461_S2019/Assignment-2-Intradomain-Routing-Algorithms. Indicate both partner's names and netIDs in a comment at the top of both files. **In addition, submit a textfile `partners.txt` that contains your netIDs (no aliases!), one per line.**

We will run the network simulation using the provided json files and additional test cases with different network architectures. Your grade will be based on whether your algorithm finds the lowest cost paths and whether you have violated any of the restrictions listed above. We will also check that `DVrouter` actually runs a distance-vector algorithm and that `LSrouter` actually runs a link-state algorithm.

As always, start early and feel free to ask questions on Piazza and in office hours.
