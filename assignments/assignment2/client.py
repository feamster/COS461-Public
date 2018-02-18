import time
import sys
import Queue
from packet import Packet


class Client:
    """Client class sends periodic "traceroute" packets and returns routes that
       these packets take back to the network object."""


    def __init__(self, addr, allClients, sendRate, updateFunction):
        """Inititaliza parameters"""
        self.addr = addr
        self.allClients = allClients
        self.sendRate = sendRate
        self.lastTime = 0
        self.link = None
        self.updateFunction = updateFunction
        self.sending = True
        self.linkChanges = Queue.Queue()
        self.keepRunning = True


    def changeLink(self, change):
        """Add a link to the client.
           The change argument should be a tuple ('add', link)"""
        self.linkChanges.put(change)


    def handlePacket(self, packet):
        """Handle receiving a packet.  If it's a routing packet, ignore.
           If it's a "traceroute" packet, update the network object with it's
           route"""
        if packet.kind == Packet.TRACEROUTE:
            self.updateFunction(packet.srcAddr, packet.dstAddr, packet.route)


    def sendTraceroutes(self):
        """Send "traceroute" packets to every other client in the network"""
        for dstClient in self.allClients:
            packet = Packet(Packet.TRACEROUTE, self.addr, dstClient)
            if self.link:
                self.link.send(packet, self.addr)
            self.updateFunction(packet.srcAddr, packet.dstAddr, [])


    def handleTime(self, timeMillisecs):
        """Send traceroute packets regularly"""
        if self.sending and (timeMillisecs - self.lastTime > self.sendRate):
            self.sendTraceroutes()
            self.lastTime = timeMillisecs


    def runClient(self):
        """Main loop of client"""
        while self.keepRunning:
            time.sleep(0.1)
            timeMillisecs = int(round(time.time() * 1000))
            try:
                change = self.linkChanges.get_nowait()
                if change[0] == "add":
                    self.link = change[1]
            except Queue.Empty:
                pass
            if self.link:
                packet = self.link.recv(self.addr)
                if packet:
                    self.handlePacket(packet)
            self.handleTime(timeMillisecs)


    def lastSend(self):
        """Send one final batch of "traceroute" packets"""
        self.sending = False
        self.sendTraceroutes()
