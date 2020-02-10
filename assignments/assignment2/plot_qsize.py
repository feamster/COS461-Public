import plot_defaults
from matplotlib.ticker import MaxNLocator
from pylab import figure
from helper import *

def plot_queue_length(f):
    to_plot=[]
    fig = figure(figsize=(16, 6))
    ax = fig.add_subplot(111)

    data = read_list(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: x - start_time, xaxis)
    qlens = map(float, col(1, data))

    xaxis = xaxis[::1]
    qlens = qlens[::1]
    ax.plot(xaxis, qlens, lw=2, color = 'red')
    ax.xaxis.set_major_locator(MaxNLocator(4))

    plt.ylabel("Packets")
    plt.grid(True)
    plt.xlabel("Seconds")
    plt.title("{}: Number of packets in queue".format(f), fontsize=16)

    plt.show()
