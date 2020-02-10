import plot_defaults
from helper import *
from collections import defaultdict

IPERF_PORT = '5001'

def first(lst):
    return map(lambda e: e[0], lst)

def second(lst):
    return map(lambda e: e[1], lst)

"""
Sample line:
2.221032535 10.0.0.2:39815 10.0.0.1:5001 32 0x1a2a710c 0x1a2a387c 11 2147483647 14592 85
"""
def parse_file(f):
    times = defaultdict(list)
    cwnd = defaultdict(list)
    srtt = []
    for l in open(f):
        fields = l.strip().split(' ')
        if len(fields) != 11:
            break
        if fields[2].split(':')[1] != IPERF_PORT:
            continue
        sport = int(fields[1].split(':')[1])
        times[sport].append(float(fields[0]))

        c = int(fields[6])
        cwnd[sport].append(c * 1480 / 1024.0)
        srtt.append(int(fields[-1]))
    return times, cwnd


def plot_cwnds(ax, f, events):
    times, cwnds = parse_file(f)
    for port in sorted(cwnds.keys()):
        t = times[port]
        cwnd = cwnds[port]

        events += zip(t, [port]*len(t), cwnd)
        ax.plot(t, cwnd)

    events.sort()

def plot_congestion_window(filename, histogram=False):
    added = defaultdict(int)
    events = []
    total_cwnd = 0
    cwnd_time = []

    min_total_cwnd = 10**10
    max_total_cwnd = 0
    totalcwnds = []

    m.rc('figure', figsize=(16, 6))
    fig = plt.figure()
    #plt.title(filename)
    plots = 1
    if histogram:
        plots = 2

    axPlot = fig.add_subplot(1, plots, 1)
    plot_cwnds(axPlot, filename, events)

    for (t,p,c) in events:
        if added[p]:
            total_cwnd -= added[p]
        total_cwnd += c
        cwnd_time.append((t, total_cwnd))
        added[p] = c
        totalcwnds.append(total_cwnd)

    axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$\sum_i W_i$")
    axPlot.grid(True)
    #axPlot.legend()
    axPlot.set_xlabel("seconds")
    axPlot.set_ylabel("cwnd KB")
    axPlot.set_title("{}: TCP congestion window (cwnd)".format(filename), fontsize=16)

    if histogram:
        axHist = fig.add_subplot(1, 2, 2)
        n, bins, patches = axHist.hist(totalcwnds, 50, normed=1, facecolor='green', alpha=0.75)

        axHist.set_xlabel("bins (KB)")
        axHist.set_ylabel("Fraction")
        axHist.set_title("Histogram of sum(cwnd_i)")

    plt.show()
