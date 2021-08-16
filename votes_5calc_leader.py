import csv
from config import config

INPUT_PATH = "./eth1_votes_final.csv"
OUTPUT_DATA_PATH = "./eth1_votes_leaders.csv"


def main():
    vote_period = int(config.SLOTS_PER_EPOCH * config.EPOCHS_PER_ETH1_VOTING_PERIOD)
    expected_max_delta = vote_period * int(config.SECONDS_PER_SLOT) * 1.5
    expected_distance = int(config.ETH1_FOLLOW_DISTANCE * config.SECONDS_PER_ETH1_BLOCK) + expected_max_delta
    latest_vote_error = 0
    vote_leaders = dict()
    next_vote_period = vote_period
    with open(OUTPUT_DATA_PATH, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        # write header
        writer.writerow(["slot", "slot_time", "eth1_block_hash", "eth1_block_number", "eth1_block_time", "leader_share"])
        with open(INPUT_PATH) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                slot = int(row[0])
                if slot >= next_vote_period:
                    next_vote_period += vote_period
                    eth1_block_hash = "0x00"
                    eth1_block_number = 0
                    leader_share = 0.0
                    delta_time = 0
                    for block_hash in vote_leaders:
                        share = vote_leaders[block_hash][1] / vote_period
                        if share > leader_share:
                            leader_share = share
                            eth1_block_hash = block_hash
                            eth1_block_number = row[3]
                            delta_time = vote_leaders[block_hash][0]
                    if delta_time > expected_distance:
                        latest_vote_error += 1
                    else:
                        latest_vote_error = 0
                    writer.writerow((row[0], row[1], eth1_block_hash, eth1_block_number, row[4], leader_share,
                                     latest_vote_error))
                    vote_leaders = dict()
                if row[2] in vote_leaders:
                    delta = int(row[1]) - int(row[4])
                    vote_leaders[row[2]] = (delta, vote_leaders[row[2]][1] + 1)
                else:
                    try:
                        delta = int(row[1]) - int(row[4])
                        vote_leaders[row[2]] = (delta, 1)
                    except:
                        pass


main()
