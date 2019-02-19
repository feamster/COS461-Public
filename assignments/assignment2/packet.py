from copy import deepcopy

class Packet:
    """Packet class defines packets that clients and routers
       send in the simulated network"""

    # Access these constants from other files
    # as Packet.TRACEROUTE or Packet.ROUTING
    TRACEROUTE = 1
    ROUTING = 2
    # Use Packet.ROUTING as the "kind" field for all packets
    # created by your implementations.


    def __init__(self, kind, srcAddr, dstAddr, content=None):
        """create a new packet"""
        self.kind = kind        # either TRACEROUTE or ROUTING
        self.srcAddr = srcAddr  # address of the source of the packet
        self.dstAddr = dstAddr  # address of the destination of the packet
        self.content = content  # content of the packet (must be a string)
        self.route = [srcAddr]  # DO NOT access from DSrouter or LSrouter


    def copy(self):
        """Create a deepcopy of the packet.  This gets called automatically
           when the packet is sent to avoid aliasing issues"""
        p = Packet(self.kind, self.srcAddr, self.dstAddr, content=deepcopy(self.content))
        p.route = list(self.route)
        return p


    def isTraceroute(self):
        """Returns True if the packet is a traceroute packet"""
        return self.kind == Packet.TRACEROUTE


    def isRouting(self):
        """Returns Trur is the packet is a routing packet"""
        return self.kind == Packet.ROUTING


    def getContent(self):
        """Returns the content of the packet"""
        return self.content


    def addToRoute(self, addr):
        '''DO NOT CALL from DVrouter or LSrouter'''
        self.route.append(addr)


    def getRoute(self):
        '''DO NOT CALL from DVRouter or LSrouter'''
        return self.route


    def animateSend(self, src, dst, latency):
        '''DO NOT CALL from DVRouter or LSrouter'''
        if hasattr(Packet, "animate"):
            Packet.animate(self, src, dst, latency)
