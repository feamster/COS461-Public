import sys
import thread
import json
import pickle
import signal
import time
import os.path
import Queue
from collections import defaultdict
from client import Client
from link import Link
from router import Router
from DVrouter import DVrouter
from LSrouter import LSrouter


class Network:
    """Network class maintains all clients, routers, links, and confguration"""

    def __init__(self, netJsonFilepath, routerClass, visualize=False):
        """Create a new network from the parameters in the file at
           netJsonFilepath.  routerClass determines whether to use DVrouter,
           LSrouter, or the default Router"""

        # parse configuration details
        netJsonFile = open(netJsonFilepath, 'r')
        netJson = json.load(netJsonFile)
        self.latencyMultiplier = 100
        self.endTime = netJson["endTime"] * self.latencyMultiplier
        self.visualize = visualize
        if visualize:
            self.latencyMultiplier *= netJson["visualize"]["timeMultiplier"]
        self.clientSendRate = netJson["clientSendRate"]*self.latencyMultiplier

        # parse and create routers, clients, and links
        self.routers = self.parseRouters(netJson["routers"], routerClass)
        self.clients = self.parseClients(netJson["clients"], self.clientSendRate)
        self.links = self.parseLinks(netJson["links"])

        # parse link changes
        if "changes" in netJson:
            self.changes = self.parseChanges(netJson["changes"])
        else:
            self.changes = None

        # parse correct routes and create some tracking fields
        self.correctRoutes = self.parseCorrectRoutes(netJson["correctRoutes"])
        self.threads = []
        self.routes = {}
        self.routesLock = thread.allocate_lock()
        netJsonFile.close()


    def parseRouters(self, routerParams, routerClass):
        """Parse routes from routerParams dict"""
        routers = {}
        for addr in routerParams:
            #print "Router {}".format(addr)
            routers[addr] = routerClass(addr, heartbeatTime=self.latencyMultiplier*10)
        return routers


    def parseClients(self, clientParams, clientSendRate):
        """Parse clients from clientParams dict"""
        clients = {}
        for addr in clientParams:
            #print "Client {}".format(addr)
            clients[addr] = Client(addr, clientParams, clientSendRate, self.updateRoute)
        return clients


    def parseLinks(self, linkParams):
        """Parse links from linkParams, dict"""
        links = {}
        for addr1, addr2, p1, p2, c12, c21 in linkParams:
            #print "{}:{} --cost:{}--> {}:{} --cost:{}--> {}:{}".format(
                   #addr1, p1, c12, addr2, p2, c21, addr1, p1)
            link = Link(addr1, addr2, c12, c21, self.latencyMultiplier)
            links[(addr1,addr2)] = (p1, p2, c12, c21, link)
        return links


    def parseChanges(self, changesParams):
        """Parse link changes from changesParams dict"""
        changes = Queue.PriorityQueue()
        for change in changesParams:
            #print change
            changes.put(change)
        return changes


    def parseCorrectRoutes(self, routesParams):
        """parse correct routes, from routesParams dict"""
        correctRoutes = defaultdict(list)
        for route in routesParams:
            src, dst = route[0], route[-1]
            correctRoutes[(src,dst)].append(route)
        return correctRoutes


    def run(self):
        """Run the network.  Start threads for each client and router. Start
           thread to track link changes.  If not visualizing, wait until
           end time and then print final routes"""
        for router in self.routers.values():
            self.threads.append(thread.start_new_thread(router.runRouter, ()))
        for client in self.clients.values():
            self.threads.append(thread.start_new_thread(client.runClient, ()))
        self.addLinks()
        if self.changes:
            thread.start_new_thread(self.handleChanges, ())
        if not self.visualize:
            time.sleep(self.endTime/float(1000))
            self.finalRoutes()
            sys.stdout.write("\n"+self.getRouteString()+"\n")


    def addLinks(self):
        """Add links to clients and routers"""
        for addr1, addr2 in self.links:
            p1, p2, c12, c21, link = self.links[(addr1, addr2)]
            if addr1 in self.clients:
                self.clients[addr1].changeLink(("add", link))
            if addr2 in self.clients:
                self.clients[addr2].changeLink(("add", link))
            if addr1 in self.routers:
                self.routers[addr1].changeLink(("add", p1, addr2, link, c12))
            if addr2 in self.routers:
                self.routers[addr2].changeLink(("add", p2, addr1, link, c21))


    def handleChanges(self):
        """Handle changes to links. Run this method in a separate thread.
           Uses a priority queue to track time of next change"""
        startTime = time.time()*1000
        while not self.changes.empty():
            changeTime, target, change = self.changes.get()
            currentTime = time.time()*1000
            waitTime = (changeTime*self.latencyMultiplier + startTime) - currentTime
            if waitTime > 0:
                time.sleep(waitTime/float(1000))
            # link changes
            if change == "up":
                addr1, addr2, p1, p2, c12, c21 = target
                link = Link(addr1, addr2, c12, c21, self.latencyMultiplier)
                self.links[(addr1,addr2)] = (p1, p2, c12, c21, link)
                self.routers[addr1].changeLink(("add", p1, addr2, link, c12))
                self.routers[addr2].changeLink(("add", p2, addr1, link, c21))
            elif change == "down":
                addr1, addr2, = target
                p1, p2, _, _, link = self.links[(addr1, addr2)]
                self.routers[addr1].changeLink(("remove", p1))
                self.routers[addr2].changeLink(("remove", p2))
            # update visualization
            if hasattr(Network, "visualizeChangesCallback"):
                Network.visualizeChangesCallback(change, target)


    def updateRoute(self, src, dst, route):
        """Callback function used by clients to update the
           current routes taken by traceroute packets"""
        self.routesLock.acquire()
        timeMillisecs = int(round(time.time() * 1000))
        isGood = route in self.correctRoutes[(src,dst)]
        try:
            _, _, currentTime = self.routes[(src,dst)]
            if timeMillisecs > currentTime:
                self.routes[(src,dst)] = (route, isGood, timeMillisecs)
        except KeyError:
            self.routes[(src,dst)] = (route, isGood, timeMillisecs)
        finally:
            self.routesLock.release()


    def getRouteString(self, labelIncorrect=True):
        """Create a string with all the current routes found by traceroute
           packets and whether they are correct"""
        self.routesLock.acquire()
        routeStrings = []
        allCorrect = True
        for src,dst in self.routes:
            route, isGood, _ = self.routes[(src,dst)]
            routeStrings.append("{} -> {}: {} {}".format(src, dst, route,
                "" if (isGood or not route or not labelIncorrect) else "Incorrect Route"))
            if not isGood:
                allCorrect = False
        routeStrings.sort()
        if allCorrect and len(self.routes) > 0:
            routeStrings.append("ALL ROUTES CORRECT!")
        routeString = "\n".join(routeStrings)
        self.routesLock.release()
        return routeString


    def getRoutePickle(self):
        """Create a pickle with the current routes
           found by traceroute packets"""
        self.routesLock.acquire()
        routePickle = pickle.dumps(self.routes)
        self.routesLock.release()
        return routePickle


    def resetRoutes(self):
        """Reset the routes foudn by traceroute packets"""
        self.routesLock.acquire()
        self.routes = {}
        self.routesLock.release()


    def finalRoutes(self):
        """Have the clients send one final batch of traceroute packets"""
        self.resetRoutes()
        for client in self.clients.values():
            client.lastSend()
        time.sleep(4*self.clientSendRate/float(1000))


def main():
    """Main function parses command line arguments and runs network"""
    if len(sys.argv) < 2:
        print "Usage: python network.py [networkSimulationFile.json] [DV|LS (router class, optional)]"
        return
    netCfgFilepath = sys.argv[1]
    routerClass = Router
    if len(sys.argv) >= 3:
        if sys.argv[2] == "DV":
            routerClass = DVrouter
        elif sys.argv[2] == "LS":
            routerClass = LSrouter
    net = Network(netCfgFilepath, routerClass, visualize=False)
    net.run()


if __name__ == "__main__":
    main()
