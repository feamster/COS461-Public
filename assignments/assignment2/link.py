import thread
import sys
import Queue
import time
import threading
from types import StringType


class Link:
    """Link class represents link between two routers/clients
       handles sending and receiving packets using
       threadsafe queues"""

    def __init__(self, e1, e2, l12, l21, latency):
        """Create queues. e1 & e2 are addresses of the 2 endpoints of
           the link. l12 and l21 are the latencies (in ms) in the
           e1->e2 and e2->e1 directions, respectively"""
        self.q12 = Queue.Queue()
        self.q21 = Queue.Queue()
        self.l12 = l12*latency
        self.l21 = l21*latency
        self.latencyMultiplier = latency
        self.e1 = e1
        self.e2 = e2


    def send_helper(self, packet, src):
        """Run in a separate thread and sends packet on
           link FROM src after waiting for the appropriate latency"""
        if src == self.e1:
            packet.addToRoute(self.e2)
            packet.animateSend(self.e1, self.e2, self.l12)
            time.sleep(self.l12/float(1000))
            self.q12.put(packet)
        elif src == self.e2:
            packet.addToRoute(self.e1)
            packet.animateSend(self.e2, self.e1, self.l21)
            time.sleep(self.l21/float(1000))
            self.q21.put(packet)
        sys.stdout.flush()


    def send(self, packet, src):
        """Sends packet on link FROM src. Checks that packet content is
           a string and starts a new thread to send it.
           (src must be equal to self.e1 or self.e2)"""
        if packet.content:
            assert type(packet.content) is StringType, "Packet content must be a string"
        p = packet.copy()
        thread.start_new_thread(self.send_helper, (p, src))


    def recv(self, dst, timeout=None):
        """Checks whether a packet is ready to be received by dst on this link.
           dst must be equal to self.e1 or self.e2.  If packet is ready, returns
           the packet, else returns None."""
        if dst == self.e1:
            try:
                packet = self.q21.get_nowait()
                return packet
            except Queue.Empty:
                return None
        elif dst == self.e2:
            try:
                packet = self.q12.get_nowait()
                return packet
            except Queue.Empty:
                return None


    def changeLatency(self, src, c):
        """Update the latency of sending on the link from src"""
        if src == self.e1:
            self.l12 = c*self.latencyMultiplier
        elif src == self.e2:
            self.l21 = c*self.latencyMultiplier
