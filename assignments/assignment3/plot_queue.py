'''
Plot queue occupancy over time
'''
from helper import *
import plot_defaults

plot_defaults.quarter_size()

from matplotlib.ticker import MaxNLocator
from pylab import figure


parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Queue timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--maxy',
                    help="Max mbps on y-axis..",
		    type=int,
                    default=500,
                    action="store",
                    dest="maxy")

parser.add_argument('--miny',
                    help="Min mbps on y-axis..",
		    type=int,
                    default=0,
                    action="store",
                    dest="miny")

parser.add_argument('--legend', '-l',
                    help="Legend to use if there are multiple plots.  File names used as default.",
                    action="store",
                    nargs="+",
                    default=None,
                    dest="legend")

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None, # Will show the plot
                    dest="out")

parser.add_argument('-s', '--summarise',
                    help="Summarise the time series plot (boxplot).  First 10 and last 10 values are ignored.",
                    default=False,
                    dest="summarise",
                    action="store_true")

parser.add_argument('--cdf',
                    help="Plot CDF of queue timeseries (first 10 and last 10 values are ignored)",
                    default=False,
                    dest="cdf",
                    action="store_true")

parser.add_argument('--labels',
                    help="Labels for x-axis if summarising; defaults to file names",
                    required=False,
                    default=[],
                    nargs="+",
                    dest="labels")

parser.add_argument('--every',
                    help="If the plot has a lot of data points, plot one every EVERY (x,y) point (default 1).",
                    default=1,
                    type=int)

args = parser.parse_args()
if args.labels is None:
    args.labels = args.files

if args.legend is None:
    args.legend = []
    for file in args.files:
        args.legend.append(file)

to_plot=[]
def get_style(i):
    if i == 0:
        return {'color': 'red'}
    else:
        return {'color': 'black', 'ls': '-.'}

print args.files
m.rc('figure', figsize=(16, 6))
fig = figure()
ax = fig.add_subplot(111)
for i, f in enumerate(args.files):
    data = read_list(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: x - start_time, xaxis)
    qlens = map(float, col(1, data))

    if args.summarise or args.cdf:
        to_plot.append(qlens[10:-10])
    else:
        xaxis = xaxis[::args.every]
        qlens = qlens[::args.every]
        ax.plot(xaxis, qlens, label=args.legend[i], lw=2, **get_style(i))

    ax.xaxis.set_major_locator(MaxNLocator(4))





#plt.title("Queue sizes")
plt.title("")
plt.ylabel("Packets")
plt.grid(True)
#yaxis = range(0, 1101, 50)
#ylabels = map(lambda y: str(y) if y%100==0 else '', yaxis)
#plt.yticks(yaxis, ylabels)
#plt.ylim((0,1100))
plt.ylim((args.miny,args.maxy))

if args.summarise:
    plt.xlabel("Link Rates")
    plt.boxplot(to_plot)
    xaxis = range(1, 1+len(args.files))
    plt.xticks(xaxis, args.labels)
    for x in xaxis:
        y = pc99(to_plot[x-1])
        print x, y
        if x == 1:
            s = '99pc: %d' % y
            offset = (-20,20)
        else:
            s = str(y)
            offset = (-10, 20)
        plt.annotate(s, (x,y+1), xycoords='data',
                xytext=offset, textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))
elif args.cdf:
    fig = figure()
    ax = fig.add_subplot(111)
    for i,data in enumerate(to_plot):
        xs, ys = cdf(map(int, data))
        ax.plot(xs, ys, label=args.legend[i], lw=2, **get_style(i))
        plt.ylabel("Fraction")
        plt.xlabel("Packets")
        plt.ylim((0, 1.0))
        #plt.legend(args.legend, loc="upper left")
        plt.title("")
        ax.xaxis.set_major_locator(MaxNLocator(4))
else:
    plt.xlabel("Seconds")
    #if args.legend:
    #    plt.legend(args.legend, loc="upper left")
    #else:
    #    plt.legend(args.files)

if args.out:
    plt.savefig(args.out)
else:
    plt.show()
