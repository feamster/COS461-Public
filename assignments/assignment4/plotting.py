import matplotlib.pyplot as plt
import numpy as np

def plot_bar(data, labelLabel, countsLabel):
    labels = [x[0] for x in data]
    counts = [x[1] for x in data]
    xvals = np.arange(len(counts))
    width = 0.9
    counts.reverse()
    labels.reverse()
    fig = plt.figure(figsize=(8,3))
    plt.barh(xvals, counts)
    plt.yticks(xvals + width/2, labels)
    plt.ylabel(labelLabel)
    plt.xlabel(countsLabel)


def plot_flows(ips_flows, k=15):
    plot_bar(ips_flows[0:k], 'Top-{} IP Addresses'.format(k), '# of Flows')


def plot_volumes(ips_volumes, k=15):
    plot_bar(ips_volumes[0:k], 'Top-{} IP Addresses'.format(k), 'Total bytes')


def plot_hosts(hosts_flows, hosts_volumes, k=15):
    plot_bar(hosts_flows[0:k], 'Top-{} Hosts'.format(k), "# of Flows")
    plot_bar(hosts_volumes[0:k], 'Top-{} Hosts'.format(k), "Total bytes")


def plot_ports(ports_flows, ports_volumes, k=15):
    plot_bar(ports_flows[0:k], 'Top-{} Ports'.format(k), "# of Flows")
    plot_bar(ports_volumes[0:k], 'Top-{} Ports'.format(k), "Total bytes")


def plot_AS(AS_flows, AS_volumes, k=15):
    plot_bar(AS_flows[0:k], 'Top-{} ASes'.format(k), "# of Flows")
    plot_bar(AS_volumes[0:k], 'Top-{} ASes'.format(k), "Total bytes")
