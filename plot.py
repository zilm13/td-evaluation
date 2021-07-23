import csv

import numpy as np
from matplotlib.image import NonUniformImage
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

INPUT_DATA_PATH = "./post_homestead_result_target.csv"


def main():
    blocks = np.array([])
    transition_miss = np.array([])
    # limit = 2000000
    skip = 9200000
    chunks = 100000
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
            transition_miss_chunk.append(int(row[6]))
            if block % chunks == 0:
                blocks = np.append(blocks, blocks_chunk)
                transition_miss = np.append(transition_miss, transition_miss_chunk)
                blocks_chunk = []
                transition_miss_chunk = []
                print("Passed #{} block".format(block))
        # latest data
        blocks = np.append(blocks, blocks_chunk)
        transition_miss = np.append(transition_miss, transition_miss_chunk)
        # dev = np.std(transition_miss, dtype=np.float64)
        # print("Deviation: {}".format(dev))
            # if block > limit:
            #     break
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


main()
