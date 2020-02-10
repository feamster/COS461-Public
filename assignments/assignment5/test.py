import sys
import threading
import time
from scapy.all import *
from scapy.all import sniff as scasniff


class PacketHandler:

    def __init__(self, intf, mac):
        self.intf = intf
        self.mac = mac
        self.num_dns = 0
        self.num_pings = 0


    def start(self):
        t = threading.Thread(target = self.sniff)
        t.start()


    def incoming(self, pkt):
        return pkt[Ether].dst == self.mac


    def handle_packet(self, pkt):
        if DNS in pkt:
            if pkt[DNS].qr == 1:
                self.num_dns += 1
        if ICMP in pkt:
            if pkt[ICMP].type == 0:
                self.num_pings += 1
        return


    def get_num_ping_replies(self):
        return self.num_pings


    def get_num_dns_responses(self):
        return self.num_dns


    def sniff(self):
        scasniff(iface=self.intf, prn = self.handle_packet,
                  lfilter = self.incoming)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: python test.py intf mac"
        sys.exit(0)

    intf = sys.argv[1]
    mac = sys.argv[2]
    handler = PacketHandler(intf, mac)
    handler.start()
    while True:
        num_dns = handler.get_num_dns_responses()
        num_pings = handler.get_num_ping_replies()
        print "{} DNS responses, {} ping replies".format(num_dns, num_pings)
        sys.stdout.flush()
        time.sleep(5)
