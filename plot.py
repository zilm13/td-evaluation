import csv

import numpy as np
from matplotlib.image import NonUniformImage
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from util import compute_target_delay_seconds

INPUT_DATA_PATH = "./post_homestead_result_target.csv"


def main():
    blocks = np.array([])
    transition_miss = np.array([])
    skip = 9200000
    chunks = 100000
    target_delay_seconds = compute_target_delay_seconds()
    print("Target delay: {} seconds".format(target_delay_seconds))
    with open(INPUT_DATA_PATH) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        blocks_chunk = []
        transition_miss_chunk = []
        for row in reader:
            block = int(row[0])
            if block < skip:
                continue
            blocks_chunk.append(block)
            # transition_miss_chunk.append(int(row[6]))  # blocks miss
            transition_miss_chunk.append((int(row[5]) - int(row[7]) - target_delay_seconds) // 60)  # seconds miss
            if block % chunks == 0:
                blocks = np.append(blocks, blocks_chunk)
                transition_miss = np.append(transition_miss, transition_miss_chunk)
                blocks_chunk = []
                transition_miss_chunk = []
                print("Passed #{} block".format(block))
        # latest data
        blocks = np.append(blocks, blocks_chunk)
        transition_miss = np.append(transition_miss, transition_miss_chunk)
        # print_deviation(transition_miss)
        # draw_histogram(blocks, transition_miss)
        # draw_percentiles(transition_miss)
        draw_simple_histogram(transition_miss)


def print_deviation(transition_miss):
    dev = np.std(transition_miss, dtype=np.float64)
    print("Deviation: {}".format(dev))
    mean = np.mean(transition_miss, dtype=np.float64)
    sigmas = [mean - 3 * dev, mean - 2 * dev, mean - dev, mean, mean + dev, mean + 2 * dev,mean + 3 * dev]
    print("-3σ,-2σ, -σ, mean, σ, 2σ, 3σ: {}".format(sigmas))
    total = np.size(transition_miss)
    between_sigmas = (((mean - dev) < transition_miss) & (transition_miss < (mean + dev))).sum()
    between_2sigmas = (((mean - (dev * 2)) < transition_miss) & (transition_miss < (mean + (dev * 2)))).sum()
    between_3sigmas = (((mean - (dev * 3)) < transition_miss) & (transition_miss < (mean + (dev * 3)))).sum()
    print("-σ..σ, {:.0f}..{:.0f}: {:.1%}".format(mean - dev, mean + dev, between_sigmas / total))
    print("-2σ..2σ, {:.0f}..{:.0f}: {:.1%}".format(mean - 2 * dev, mean + 2 * dev,between_2sigmas / total))
    print("-3σ..3σ, {:.0f}..{:.0f}: {:.1%}".format(mean - 3 * dev, mean + 3 * dev,between_3sigmas / total))
    minus_sigmas = (((mean - dev) < transition_miss) & (transition_miss < 0)).sum()
    minus_2sigmas = (((mean - (dev * 2)) < transition_miss) & (transition_miss < 0)).sum()
    minus_3sigmas = (((mean - (dev * 3)) < transition_miss) & (transition_miss < 0)).sum()
    print("-σ..0, {:.0f}..{:.0f}: {:.1%}".format(mean - dev, 0, minus_sigmas / total))
    print("-2σ..0, {:.0f}..{:.0f}: {:.1%}".format(mean - 2 * dev, 0, minus_2sigmas / total))
    print("-3σ..0, {:.0f}..{:.0f}: {:.1%}".format(mean - 3 * dev, 0, minus_3sigmas / total))
    plus_sigmas = ((0 <= transition_miss) & (transition_miss < (mean + dev))).sum()
    plus_2sigmas = ((0 <= transition_miss) & (transition_miss < (mean + 2 * dev))).sum()
    plus_3sigmas = ((0 <= transition_miss) & (transition_miss < (mean + 3 * dev))).sum()
    print("0..σ, {:.0f}..{:.0f}: {:.1%}".format(0, mean + dev, plus_sigmas / total))
    print("0..2σ, {:.0f}..{:.0f}: {:.1%}".format(0, mean + 2 * dev, plus_2sigmas / total))
    print("0..3σ, {:.0f}..{:.0f}: {:.1%}".format(0, mean + 3 * dev, plus_3sigmas / total))


def draw_histogram(blocks, transition_miss):
    H, xedges, yedges = np.histogram2d(blocks, transition_miss, bins=[200,250])
    # Histogram does not follow Cartesian convention (see Notes),
    # therefore transpose H for visualization purposes.
    H = H.T
    fig = plt.figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111, title='Transition block calculation miss (post-Muir, 13 seconds block)',
                         aspect='auto', xlim=xedges[[0, -1]], ylim=yedges[[0, -1]])
    ax.get_xaxis().set_major_formatter(
        FuncFormatter(lambda x, p: format(int(x), ',')))
    im = NonUniformImage(ax)
    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2
    im.set_data(xcenters, ycenters, H)
    ax.images.append(im)
    # Turn off exponential values for X-axis
    plt.show()


def draw_percentiles(transition_miss):
    p = np.linspace(0, 100, 6001)
    ax = plt.gca()
    ax.plot(p, np.percentile(transition_miss, p, interpolation='linear'), linestyle=None)
    ax.set(
        title='Percentiles for transition miss',
        xlabel='Percentile',
        ylabel='Miss',
        yticks=[np.amin(transition_miss), -4021.1050902662396, -2795.5493173614295, -1569.9935444566195,
                -344.4377715518094, 0,
                881.1180013530006, 2106.6737742578107, 3332.2295471626207, np.amax(transition_miss)]
    )
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels[0] = np.amin(transition_miss)
    labels[1] = '-3σ'
    labels[2] = '-2σ'
    labels[3] = '-σ'
    labels[4] = 'mean'
    labels[5] = 0
    labels[6] = 'σ'
    labels[7] = '2σ'
    labels[8] = '3σ'
    labels[9] = np.amax(transition_miss)
    ax.set_yticklabels(labels)
    ax.legend()
    plt.show()


def draw_simple_histogram(transition_miss):
    _ = plt.hist(transition_miss, bins=20)
    plt.title("Transition miss in minutes histogram")
    plt.show()


main()
