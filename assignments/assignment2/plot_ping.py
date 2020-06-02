import plot_defaults
from matplotlib.ticker import MaxNLocator
from pylab import figure
from helper import *

def parse_ping(fname):
    ret = []
    lines = open(fname).readlines()
    num = 0
    for line in lines:
        if 'bytes from' not in line:
            continue
        try:
            rtt = line.split(' ')[-2]
            rtt = rtt.split('=')[1]
            rtt = float(rtt)
            ret.append([num, rtt])
            num += 1
        except:
            break
    return ret

def plot_ping_rtt(f, freq=10):
    fig = figure(figsize=(16, 6))
    ax = fig.add_subplot(111)

    data = parse_ping(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: (x - start_time) / freq, xaxis)
    qlens = map(float, col(1, data))

    ax.plot(xaxis, qlens, lw=2)
    ax.xaxis.set_major_locator(MaxNLocator(4))

    plt.ylabel("RTT (ms)")
    plt.xlabel("time (seconds)")
    plt.grid(True)
    plt.title("{}: RTT from pings".format(f), fontsize=16)

    plt.show()
