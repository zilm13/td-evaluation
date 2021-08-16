import csv
from config import config

INPUT_PATH = "./eth1_votes_no_outliers.csv"
OUTPUT_DATA_PATH = "./eth1_votes_period_sec.csv"


def main():
    delta_seconds = int(config.SECONDS_PER_SLOT * config.EPOCHS_PER_ETH1_VOTING_PERIOD * config.SLOTS_PER_EPOCH)
    with open(OUTPUT_DATA_PATH, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        # write header
        writer.writerow(["slot", "slot_time", "eth1_block_hash", "eth1_block_number", "eth1_block_time", "delta",
                         "delta_minus_follow", "previous_period_miss"])
        previous_block_time = 0
        with open(INPUT_PATH) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], int(row[4]) - previous_block_time
                                 - delta_seconds - int(config.SECONDS_PER_ETH1_BLOCK)))
                previous_block_time = int(row[4])


main()
