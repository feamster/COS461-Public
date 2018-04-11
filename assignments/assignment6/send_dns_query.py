import sys
from scapy.all import * 
from time import sleep
import random

def SendDnsQuery(src_ip, dns_srv, sleep_time):
    random.seed()
    sleep(5)
    while True:
        qid = random.randint(0, 2 ** 16 - 1)
        p=(IP(src=src_ip,dst=dns_srv)/UDP(sport = random.randint(1025, 2 ** 16 - 1))/DNS(id = qid, rd=0,qd=DNSQR(qtype="ANY", qname="cos461.net")))
        send(p)
        sleep(sleep_time)

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: python send_dns_query.py src_ip dns_srv_ip sleep_time"
                sys.exit(0)
                
	SendDnsQuery(sys.argv[1], sys.argv[2], float(sys.argv[3]))


