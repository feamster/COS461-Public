from time import sleep, time
from subprocess import *
import re

default_dir = '.'

def monitor_qlen(iface, interval_sec = 0.01, fname='%s/qlen.txt' % default_dir):
    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    ret = []
    open(fname, 'w').write('')
    while 1:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        # Not quite right, but will do for now
        matches = pat_queued.findall(output)
        if matches and len(matches) > 1:
            ret.append(matches[1])
            t = "%f" % time()
            open(fname, 'a').write(t + ',' + matches[1] + '\n')
        sleep(interval_sec)
    #open('qlen.txt', 'w').write('\n'.join(ret))
    return

def monitor_devs_ng(fname="%s/txrate.txt" % default_dir, interval_sec=0.01):
    """Uses bwm-ng tool to collect iface tx rate stats.  Very reliable."""
    cmd = ("sleep 1; bwm-ng -t %s -o csv "
           "-u bits -T rate -C ',' > %s" %
           (interval_sec * 1000, fname))
    Popen(cmd, shell=True).wait()
