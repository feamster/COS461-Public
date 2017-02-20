####################################################
# LSrouter.py
# Names:
# NetIds:
#####################################################

import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class LSrouter(Router):
    """Link state routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove


    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        pass


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        pass


    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        pass


    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        pass


    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return ""
