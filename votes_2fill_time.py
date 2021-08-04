import csv
from config import config

BLOCKS_TIME= "./blocks_4_mainnet.csv"
VOTES_PATH = "./eth1_votes.csv"
OUTPUT_DATA_PATH = "./eth1_votes_final.csv"


def main():
    time_data = dict()
    skip = 11320898
    with open(BLOCKS_TIME) as rp:
        reader = csv.reader(rp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            block = int(row[0])
            if block < skip:
                continue
            time_data[row[0]] = int(row[2])
    print("All time data readed, writing!")
    with open(OUTPUT_DATA_PATH, "wt") as wp:
        writer = csv.writer(wp, delimiter=",")
        # write header
        writer.writerow(["slot", "slot_time", "eth1_block_hash", "eth1_block_number", "eth1_block_time"])
        with open(VOTES_PATH) as rp:
            reader = csv.reader(rp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                slot_time = config.SECONDS_PER_SLOT * int(row[0]) + config.MIN_GENESIS_TIME
                writer.writerow((row[0], slot_time, row[1], row[2], time_data.get(row[2], "None")))


main()
