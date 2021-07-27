from remerkleable.basic import uint256
from remerkleable.complex import Container
from config import config


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


def compute_target_delay() -> int:
    seconds_per_voting_period = config.EPOCHS_PER_ETH1_VOTING_PERIOD * config.SLOTS_PER_EPOCH \
                                * config.SECONDS_PER_SLOT
    pow_blocks_per_voting_period = seconds_per_voting_period // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_to_merge = config.TARGET_SECONDS_TO_MERGE // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_after_anchor_block = config.ETH1_FOLLOW_DISTANCE + pow_blocks_per_voting_period + pow_blocks_to_merge
    return int(pow_blocks_after_anchor_block)


def compute_target_delay_seconds() -> int:
    seconds_per_voting_period = config.EPOCHS_PER_ETH1_VOTING_PERIOD * config.SLOTS_PER_EPOCH \
                                * config.SECONDS_PER_SLOT
    pow_blocks_per_voting_period = seconds_per_voting_period // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_to_merge = config.TARGET_SECONDS_TO_MERGE // config.SECONDS_PER_ETH1_BLOCK
    pow_blocks_after_anchor_block = config.ETH1_FOLLOW_DISTANCE + pow_blocks_per_voting_period + pow_blocks_to_merge
    return int(pow_blocks_after_anchor_block * config.SECONDS_PER_ETH1_BLOCK)
