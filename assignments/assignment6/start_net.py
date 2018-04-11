from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.cli import CLI
from mininet.node import OVSController

from subprocess import Popen
from time import sleep

class TestTopo(Topo):

    def __init__(self):
        super(TestTopo, self).__init__()
        self.addHost('h1', ip = "10.0.0.1", mac = "00:00:00:00:00:01")
        self.addHost('h2', ip = "10.0.0.2",  mac = "00:00:00:00:00:02")
        self.addHost('h3', ip = "10.0.0.3",  mac = "00:00:00:00:00:03")
        self.addHost('h4', ip = "10.0.0.4",  mac = "00:00:00:00:00:04")

        self.addSwitch('s1')
        self.addSwitch('s2')

        self.addHost('mb', ip="10.0.0.5", inNamespace = False)

        self.addLink('s2', 'h3')
        self.addLink('s2', 'h2')
        self.addLink('s1', 'h1')
        self.addLink('s1', 'h4')

        self.addLink('s1', 'mb')
        self.addLink('s2', 'mb')


def setup(net):
    for h in net.hosts:
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")


if __name__ == "__main__":
    topo = TestTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, controller = OVSController)
    s1 = net.getNodeByName('s1')
    s1.setMAC("00:00:00:00:00:10", intf = "s1-eth3")

    s2 = net.getNodeByName('s2')
    s2.setMAC("00:00:00:00:00:20", intf = "s2-eth3")

    net.start()
    setup(net)

    # mb is the middlebox
    mb = net.getNodeByName("mb")
    mb.popen("python mb.py > mb-log.txt 2> mb-err.txt", shell=True)
    sleep(3)
    
    # h3 is the name server
    h3 = net.getNodeByName("h3")
    h3.popen("/etc/init.d/bind9 stop > /dev/null", shell=True)
    h3.popen("/etc/init.d/bind9 start > /dev/null", shell=True)

    # h1 is the victim
    h1 = net.getNodeByName("h1")
    h1.popen("python legit_dns_traffic.py 10.0.0.3 5 > /dev/null &", shell=True)
    h1.popen("ping 10.0.0.3 -i 2 > h1_ping.txt &", shell=True)
    h1.popen("python test.py h1-eth0 00:00:00:00:00:01 > h1_test.txt &", shell=True)

    # h4 is a regular host
    h4 = net.getNodeByName("h4")
    h4.popen("python legit_dns_traffic.py 10.0.0.3 5 > /dev/null &", shell=True)
    h4.popen("ping 10.0.0.3 -i 2 > h4_ping.txt &", shell=True)
    h4.popen("python test.py h4-eth0 00:00:00:00:00:04 > h4_test.txt &", shell=True)

    # h2 is the attacker
    h2 = net.getNodeByName("h2")
    h2.popen("python send_dns_query.py 10.0.0.1 10.0.0.3 0.5 > /dev/null &", shell=True)

    CLI(net)
    h3.cmd("/etc/init.d/bind9 stop > /dev/null")
    net.stop()

    Popen("pgrep -f python | xargs kill -9", shell=True).wait()
    Popen("pgrep -f dns | xargs kill -9", shell=True).wait()
    Popen("pgrep -f ping | xargs kill -9", shell=True).wait()
