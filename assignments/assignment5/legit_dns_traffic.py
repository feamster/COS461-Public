import sys
from subprocess import call
from time import sleep

def SendDnsQuery(dns_srv, sleep_time):
    sleep(5)
    while True:
        call(["dig", "@%s" % dns_srv, "ANY", "cos461.net"]) 
        sleep(sleep_time)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python send_recv_dns.py dns_srv_ip sleep_time"
        sys.exit(0)
    SendDnsQuery(sys.argv[1], float(sys.argv[2]))


