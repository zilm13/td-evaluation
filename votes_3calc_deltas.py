import csv
from config import config

INPUT_PATH = "./eth1_votes_final.csv"
OUTPUT_DATA_PATH = "./eth1_votes_clean.csv"


def main():
    with open(OUTPUT_DATA_PATH, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        # write header
        writer.writerow(["slot", "slot_time", "eth1_block_hash", "eth1_block_number", "eth1_block_time", "delta",
                         "delta_minus_follow"])
        latest_eth1_block = 0
        with open(INPUT_PATH) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                temp_block = 0
                try:
                    temp_block = int(row[3])
                except:
                    pass
                if temp_block > latest_eth1_block:
                    delta = int(row[1]) - int(row[4])
                    writer.writerow((row[0], row[1], row[2], row[3], row[4], delta,
                                     delta - config.ETH1_FOLLOW_DISTANCE * config.SECONDS_PER_ETH1_BLOCK))
                    latest_eth1_block = temp_block


main()
