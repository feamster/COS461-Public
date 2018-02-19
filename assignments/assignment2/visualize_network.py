import sys
from Tkinter import *
import tkFont
import json
import thread
import time
from router import Router
from network import Network
from packet import Packet
from link import Link
from DVrouter import DVrouter
from LSrouter import LSrouter


class App:
    """Tkinter GUI application for network simulation visualizations"""

    def __init__(self, root, network, networkParams):
        self.network = network
        self.networkParams = networkParams
        Packet.animate = self.packetSend
        Network.visualizeChangesCallback = self.visualizeChanges
        self.animateRate = networkParams["visualize"]["animateRate"]
        self.latencyCorrection = networkParams["visualize"]["latencyCorrection"]
        self.clientFollowing = None
        self.routerFollowing = None
        self.displayCurrentRoutesRate = 100
        self.displayCurrentDebugRate = 50

        # enclosing frame
        self.frame = Frame(root)
        self.frame.grid(padx=10, pady=10)

        # canvas for drawing network
        self.canvasWidth = networkParams["visualize"]["canvasWidth"]
        self.canvasHeight = networkParams["visualize"]["canvasHeight"]
        self.canvas = Canvas(self.frame, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.grid(column=1, row=1, rowspan=4)

        # text for displaying current routes
        self.routeLabel = Label(self.frame, text="Current routes:")
        self.routeLabel.grid(column=3, row=1)
        self.routeScrollbar = Scrollbar(self.frame)
        self.routeScrollbar.grid(column=2, row=2, sticky=NE+SE)
        self.routeText = Text(self.frame, yscrollcommand=self.routeScrollbar.set)
        self.routeText.grid(column=3, row=2)

        # text for displaying debugging information
        self.debugLabel = Label(self.frame, text="Click on routers to print debug string below:")
        self.debugLabel.grid(column=3, row=3)
        self.debugScrollbar = Scrollbar(self.frame)
        self.debugScrollbar.grid(column=2, row=4, sticky=NE+SE)
        self.debugText = Text(self.frame, yscrollcommand=self.debugScrollbar.set)
        self.debugText.grid(column=3, row=4)

        self.rectCenters = self.calcRectCenters()
        self.lines, self.lineLabels = self.drawLines()
        self.rects = self.drawRectangles()

        #self.drawNetwork()
        thread.start_new_thread(self.network.run, ())
        thread.start_new_thread(self.displayCurrentRoutes, ())
        thread.start_new_thread(self.displayCurrentDebug, ())

    def calcRectCenters(self):
        """Compute the centers of the rectangles representing clients/routers"""
        rectCenters = {}
        gridSize = int(self.networkParams["visualize"]["gridSize"])
        self.boxWidth = self.canvasWidth / gridSize
        self.boxHeight = self.canvasHeight / gridSize
        for label in self.networkParams["visualize"]["locations"]:
            gx,gy = self.networkParams["visualize"]["locations"][label]
            rectCenters[label] = (gx*self.boxWidth + self.boxWidth/2,
                                  gy*self.boxHeight + self.boxHeight/2)
        return rectCenters


    def drawLines(self):
        """draw lines corresponding to links"""
        lines = {}
        lineLabels = {}
        for addr1, addr2, p1, p2, c12, c21 in self.networkParams["links"]:
            line, lineLabel = self.drawLine(addr1, addr2, c12, c21)
            lines[(addr1, addr2)] = line
            lineLabels[(addr1, addr2)] = lineLabel
        return lines, lineLabels


    def drawLine(self, addr1, addr2, c12, c21):
        """draw a single line corresponding to one link"""
        center1, center2 = self.rectCenters[addr1], self.rectCenters[addr2]
        line = self.canvas.create_line(center1[0], center1[1], center2[0], center2[1],
                                       width=self.networkParams["visualize"]["lineWidth"], fill=self.networkParams["visualize"]["lineColor"])
        self.canvas.tag_lower(line)
        tx, ty = (center1[0] + center2[0])/2, (center1[1] + center2[1])/2
        t = str(c12) if c12 == c21 else "{}->{}:{}, {}->{}:{}".format(addr1, addr2, c12, addr2, addr1, c21)
        label = self.canvas.create_text(tx, ty, text=t,
                                       state=NORMAL, font=tkFont.Font(size=self.networkParams["visualize"]["lineFontSize"]))
        return line, label


    def drawRectangles(self):
        """draw rectangles corresponding to clients/routers"""
        rects = {}
        for label in self.rectCenters:
            if label in self.network.clients:
                fill = self.networkParams["visualize"]["clientColor"]
            elif label in self.network.routers:
                fill = self.networkParams["visualize"]["routerColor"]
            c = self.rectCenters[label]
            rect = self.canvas.create_rectangle(c[0]-self.boxWidth/6, c[1]-self.boxHeight/6,
                    c[0]+self.boxWidth/6, c[1]+self.boxHeight/6, fill=fill, activeoutline="green", activewidth=5)
            self.canvas.tag_bind(rect, '<1>', lambda event, label=label: self.inspectClientOrRouter(label))
            rects[label] = rect
            rectText = self.canvas.create_text(c[0], c[1], text=label, font=tkFont.Font(size=18, weight='bold'))
        return rects


    def inspectClientOrRouter(self, addr):
        """Handle a mouse click on a client or router"""
        if addr in self.network.clients:
            if self.clientFollowing:
                self.canvas.itemconfig(self.rects[self.clientFollowing], width=1)
            if self.clientFollowing != addr:
                self.clientFollowing = addr
                self.canvas.itemconfig(self.rects[addr], width=7)
            else:
                self.clientFollowing = None
        elif addr in self.network.routers:
            if self.routerFollowing:
                self.canvas.itemconfig(self.rects[self.routerFollowing], outline='black', width=1)
            if self.routerFollowing != addr:
                self.routerFollowing = addr
                self.canvas.itemconfig(self.rects[addr], width=7)
            else:
                self.routerFollowing = None


    def packetSend(self, packet, src, dst, latency):
        """Callback function used by Packet to tell the visualization that
           a packet is being sent"""
        if self.clientFollowing:
            if packet.dstAddr == self.clientFollowing and packet.isTraceroute():
                fillColor = "green"
            else:
                 return
        else:
            fillColor = "gray" if packet.isTraceroute() else "turquoise"
        latency = latency/self.latencyCorrection
        cx, cy = self.rectCenters[src]
        dx, dy = self.rectCenters[dst]
        packetRect = self.canvas.create_rectangle(cx-6, cy-6, cx+6, cy+6, fill=fillColor)
        distx, disty = dx-cx, dy-cy
        velocityx, velocityy = (distx*self.animateRate)/float(latency), (disty*self.animateRate/float(latency))
        numSteps, stepTime = latency / self.animateRate, self.animateRate/float(1000)
        thread.start_new_thread(self.movePacket, (packetRect, velocityx, velocityy, numSteps, stepTime))


    def movePacket(self, packetRect, vx, vy, numSteps, stepTime):
        """Animate a moving packet.  This should be run on a separate thread"""
        s = numSteps
        while s > 0:
            time.sleep(stepTime)
            self.canvas.move(packetRect, vx, vy)
            s -= 1
        self.canvas.delete(packetRect)


    def displayCurrentRoutes(self):
        """Display the current routes found by traceroute packets"""
        while True:
            routeString = self.network.getRouteString(labelIncorrect=False)
            pos = self.routeScrollbar.get()
            self.routeText.delete(1.0,END)
            self.routeText.insert(1.0, routeString)
            self.routeText.yview_moveto(pos[0])
            time.sleep(self.displayCurrentRoutesRate/float(1000))


    def displayCurrentDebug(self):
        """Display the debug string of the currently selected router"""
        while True:
            if self.routerFollowing:
                debugText = self.network.routers[self.routerFollowing].debugString()
                pos = self.debugScrollbar.get()
                self.debugText.delete(1.0,END)
                self.debugText.insert(END, debugText + "\n")
                self.debugText.yview_moveto(pos[0])
            time.sleep(self.displayCurrentDebugRate/float(1000))


    def visualizeChanges(self, change, target):
        """Make color and text changes to links upon additions, removals,
           and cost changes"""
        if change == "up":
            addr1, addr2, _, _, c12, c21 = target
            newLine, newLabel = self.drawLine(addr1, addr2, c12, c21)
            self.lines[(addr1, addr2)] = newLine
            self.linesLabel = newLabel
        elif change == "down":
            addr1, addr2, = target
            self.canvas.delete(self.lines[(addr1, addr2)])
            self.canvas.delete(self.lineLabels[(addr1, addr2)])


def main():
    """Main function parses command line arguments and
       runs the network visualizer"""
    if len(sys.argv) < 2:
        print "Usage: python network.py [networkSimulationFile.json] [DV|LS (router class, optional)]"
        return
    netCfgFilepath = sys.argv[1]
    visualizeParams = json.load(open(netCfgFilepath))
    routerClass = Router
    if len(sys.argv) == 3:
        if sys.argv[2] == "DV":
            routerClass = DVrouter
        elif sys.argv[2] == "LS":
            routerClass = LSrouter
    net = Network(netCfgFilepath, routerClass, visualize=True)
    root = Tk()
    root.wm_title("Network Visualization")
    app = App(root, net, visualizeParams)
    root.mainloop()


if __name__ == "__main__":
    main()
