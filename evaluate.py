import csv

from remerkleable.basic import uint256
from remerkleable.complex import Container
from config import config

DIFFICULTY_DATA_PATH = "./blocks_4_mainnet.csv"
RESULT_OUTPUT_DATA_PATH = "./result.csv"


class PowBlock(Container):
    difficulty: uint256
    total_difficulty: uint256


def compute_transition_total_difficulty(anchor_pow_block: PowBlock) -> uint256:
    seconds_per_voting_period = config.EPOCHS_PER_ETH1_VOTING_PERIOD * config.SLOTS_PER_EPOCH \
                                * config.SECONDS_PER_SLOT
    pow_blocks_per_voting_period = seconds_per_voting_period // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_to_merge = config.TARGET_SECONDS_TO_MERGE // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_after_anchor_block = config.ETH1_FOLLOW_DISTANCE + pow_blocks_per_voting_period + pow_blocks_to_merge
    anchor_difficulty = max(config.MIN_ANCHOR_POW_BLOCK_DIFFICULTY, anchor_pow_block.difficulty)

    return anchor_pow_block.total_difficulty + uint256(anchor_difficulty) * uint256(pow_blocks_after_anchor_block)


def main():
    total_difficulty = 0
    result_log = 100000
    with open(RESULT_OUTPUT_DATA_PATH, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        # write header
        writer.writerow(["block", "difficulty", "total_difficulty", "transition_total_difficulty", "timestamp"])
        with open(DIFFICULTY_DATA_PATH) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                total_difficulty += int(row[1])
                block = PowBlock(difficulty=int(row[1]), total_difficulty=total_difficulty)
                transition_total_difficulty = compute_transition_total_difficulty(block)
                writer.writerow((row[0], row[1], total_difficulty, transition_total_difficulty, row[2]))
                if int(row[0]) % result_log == 0:
                    print("Calculated {} blocks".format(row[0]))


main()
