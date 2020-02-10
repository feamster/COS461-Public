import sys
import matplotlib.pyplot as plt
import numpy as np


def parse_test_output(fname):
    f = open(fname, 'r')
    num_dns = []
    for line in f:
        try:
            count  = int(line.split(' ')[0])
            num_dns.append(count)
        except ValueError:
            pass
    f.close()
    return num_dns


def plot_dns(fnames):
    # plot absolute # responses received
    fig = plt.figure(figsize=(16,8))
    for fname in fnames:
        data = parse_test_output(fname)
        plt.plot(np.arange(len(data))*5, data, linewidth=2, label=fname.split('.')[0].split('_')[0])
    plt.legend(fontsize=16, loc=2)
    plt.xlabel("Seconds (approximate)", fontsize=16)
    plt.ylabel("Number of DNS responses received", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig("DNS_response_rates.png")


if __name__ == "__main__":
    test_fnames = ['h1_test.txt', 'h4_test.txt']
    plot_dns(test_fnames)
    #plt.show()
