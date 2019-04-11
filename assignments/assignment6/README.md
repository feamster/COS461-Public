# Assignment 6: Network Security - DNS Reflection

### Due April 22nd, 5:00pm

DNS reflection/amplification attacks are a specific kind of DDoS attack that use DNS servers to flood a victim service or host with many DNS reply packets. In this assignment, you will learn a technique to detect and mitigate DNS reflection attacks and will apply this techniques on an emulated mininet network.

You should work with a partner on this assignment.

## Background

### Attack Description

In a DNS reflection attack, an attacker sends a DNS request to a DNS server with the source IP address spoofed to the victim's IP address. The DNS server then sends the reply to the victim. The attacker can use many compromised machines (botnets) to generate a very large number of such requests, which results in an overwhelming amount of traffic (DNS responses) headed towards the victim's machine.

In addition to this reflection component, the attack also involves "amplification." The size of each DNS response is typically larger than the size of each corresponding request. As a result, even if the attacker launches the attack from a single compromised machine, the attack will result in more traffic (by bytes) reaching the victim than was sent by the attacker. The amplification effect, and therefore the power of the attack, becomes even more pronounced when the attack is launched from many machines.

### Detection

One way to detect DNS reflection attacks is to keep track of the DNS requests and responses that each host sends and receives. Suppose there is a middlebox at the edge of a network that has sufficient resources to process DNS traffic as it passes through the network.
This middlebox can record, for each host, the identification number of each outgoing DNS query.  If a DNS response's identification number does not match any of the at-large requests recorded for its destination, the middlebox will increment a counter. If the counter passes some threshold, the middlebox may determine that the host is receiving unsolicited responses and is thus a victim of a reflection attack.

### Mitigation

One way to mitigate DNS reflection is to rate-limit the attack traffic. More specifically, in the scenario described above, once the middlebox detects an attack towards a specific host, it can limit the rate of DNS responses that the host receives. One could think of completely blocking the traffic, but in the case of DNS, there could be some legitimate DNS responses that the host asked for and needs for maintaining its connection to the network.

## Part A: Network Setup

On your host machine (not the VM), go to the course assignments directory:

```
$ cd COS461-Public/assignments
```
 Pull the latest update from Github:
```
$ git pull
```

Reprovision your VM to install necessary packages for this assignment:

```
$ vagrant reload --provision
```

You can then run `vagrant ssh` like usual.
Running `sudo python start_net.py` from your vagrant VM terminal will setup the network shown in Fig. 1 in mininet. The start_net.py script opens a mininet command line interface (CLI) once the network is up and running. You can use mininet CLI commands to get network information and interact with the hosts and switches on your network if needed.
Typing `help` into the mininet CLI will give you a list of available commands. To gracefully end the experiment, you should type `quit` on the mininet CLI. That takes care of cleaning up mininet and all the processes it has started. If it exited with an exception, or if attempting to start the simulation in the first place gave you an error, run the script `./cleanup_mininet.sh` (if permission is denied, run `chmod 744 cleanup_mininet.sh` first to change permissions).

<figure>
    <img width=700 src="figures/network.png">
    <figcaption>
        <b>Fig 1. &#8211 Mininet configuration</b>
    </figcaption>
</figure>

In this setup, **s1**, **h1**, and **h4** constitute your private network. **mb** is the middlebox sitting at the  edge; this middlebox can see all the incoming and outgoing traffic of your network. **h3** is a host that is running `bind`, an open DNS resolver, and **h2** is an attacker. Middlebox **mb** has two interfaces, **mb-eth0** connecting to s1 and **mb-eth1** connectiong to s2.

Once you start the network, h1 and h4 begin to send DNS requests every 5 seconds and pings every 2 seconds to the DNS resolver (h3). At the same time, h2 starts sending *spoofed* DNS requests on behalf of h1 to the DNS resolver every half a second. Thus, h1 is going to be the victim of a DNS reflection attack.

## Part B: Detection & Mitigation
The middlebox in the simulated network topology runs the python script  `mb.py`. This script uses a python library called Scapy to sniff packets from the two interfaces of the middlebox, applies the `handle_packet()` method to each packet, and sends the packet out on the correct interface.  You have to add code to the sections of `mb.py`  marked `TODO` in order to implement the DNS reflection attack detection and mitigation strategy described in the "Background" section above. Do not modify any existing code in `mb.py` because it is necessary for correct packet routing.

### Detection
For DNS reflection detection, check each packet going through the middlebox and out interface mb-eth1 (toward h2 & h3) to see if it is a DNS request. If it is, record a mapping from the request's identification number to the source IP of the request.

For each DNS response packet going through the middlebox and out interface mb-eth0 (toward h1 & h4), check whether there has been a request with the same identification number from the destination IP of the response. Keep track of the total number of unmatched responses sent to each host. If this number passes **200** for any host, mitigation should be started for that host (see "Mitigation" below).

There are 2 `TODO` sections in `mb.py`. The first is in the constructor `__init__()`.  This is where you should create any instance variables needed for the detection algorithm. These instance variables should start with the keyword `self`, (e.g. `self.id_to_host`). For more information on Python classes, see the documentation here: [A first look at classes](https://docs.python.org/2.7/tutorial/classes.html#a-first-look-at-classes)

The second `TODO` is in the `handle_packet()` method. Here, you will need to update the instance variables in response to the contents of the current packet. The `pkt` argument is the current packet encoded in the Scapy packet format. The following example shows how to access the source and destination IP addresses of `pkt`:

```
# check whether pkt is an IP packet
if IP in pkt:

  # get source IP addresses
  src_ip = pkt[IP].src

  # get destionation IP addresses
  dst_ip = pkt[IP].dst

```

The following example shows how check whether a DNS packet is a request or a response and how to get its ID:

```
# check whether pkt is a DNS packet
if DNS in pkt:

  # check if pkt is a DNS response or request
  is_response = pkt[DNS].qr == 1
  is_request = pkt[DNS].qr == 0

  # get ID of DNS request/response
  dns_id = pkt[DNS].id
```

Scapy is a powerful packet manipulation tool that allows you to do more than just inspect packets (although that's all you will be using it for in this assignment).  For more information about Scapy, see the documentation here: https://www.secdev.org/projects/scapy/doc/usage.html

### Mitigation

Once you detect that a host is being attacked, begin rate limiting DNS response traffic sent out of the middlebox to that specific host.

Implement rate limiting by randomly dropping DNS response packets headed to the victim host with high probability `P`. Use the `random()` function to generate random numbers, documentation here: https://docs.python.org/2/library/random.html.  The value `P` is up to you.  You will be asked to justify the value you chose in the last part of the assignment.  Drop packets by returning from the  within the `handle_packet()` method before the `sendp()` call.  

You should make sure you are only rate limiting attack traffic. Do not rate limit DNS responses to requests actually made by the victim host. Traffic to and from other hosts as well as other types of traffic to the victim host should not be rate limited either.

**Note:** Although in this specific setup h1 is the victim, we may test your assignment using h4 as victim. Therefore, your detection and mitigation implementation should not assume a specific host to be victim. Moreover, you should not have h1 (or h4's) specific details (such as IP address) or the rates at which the traffic is generated hardcoded in your code.

## Part C: Run Simulation

Run your implementation with the command

```
sudo python start_net.py
```

This will create the network and run the detection/mitigation code described in the previous sections. Hosts h1 and h4 will also run the `test.py` script.  The script sniffs all the packets sent to the host on which the script is running, keeps track of the number of DNS responses and ping replies, and prints them to `h1_test.txt` or `h4_test.txt` every 5 seconds.

Allow the simulation to run for several minutes (approximately 5 min should be fine).  Exit the simulation with the `quit` command in the mininet CLI.

If the simulation works, you will see that the `h1_ping.txt`, and  `h4_ping.txt` files have a record of successful pings and the `h1_test.txt` and `h4_test.txt` files have a record of DNS responses and pings.

Finally, run
```
python plot_results.py
```
to plot DNS response counts and save the plot to `DNS_response_rates.png`. You will need to refer to this plot in Part D below.  

**Debugging Tips:**
1. To debug your code in `mb.py`, you can print informative messages to stdout using `print(message)`.  These messages will be automatically redirected to the `mb-log.txt` file.  Please remove these prints before submitting.  Stderr for `mb.py` will automatically print to `mb-err.txt`.
2. Make sure you are checking whether a packet is a DNS packet before attempting to access its src/dst IP address or its DNS ID.
3. Remember to run `./cleanup-mininet.sh` if your program crashes, mininet exits with an exception, or you get "Please shut down the controller which is running" errors.
4. If you start getting strange errors related to creating threads, `logout` of vagrant, run `vagrant halt` and then `vagrant up` to reboot your VM.

## Part D: Analysis
Answer the questions in the file `questions.txt`.  Put your and your partner's names and netids at the top of the file.

## Submission & Grading
Submit your `mb.py`, `questions.txt`, and `DNS_response_rates.png` files to CS DropBox here: https://dropbox.cs.princeton.edu/COS461_S2019/Assignment-6-DNS-Reflection.

We will run the simulation with your `mb.py` file to test your DNS reflection detection and mitigation implementation.
