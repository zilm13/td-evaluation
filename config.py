from typing import NamedTuple
from remerkleable.basic import uint64


class Configuration(NamedTuple):
    SECONDS_PER_SLOT: uint64
    SECONDS_PER_ETH1_BLOCK: uint64
    EPOCHS_PER_ETH1_VOTING_PERIOD: uint64
    SLOTS_PER_EPOCH: uint64
    ETH1_FOLLOW_DISTANCE: uint64
    MIN_ANCHOR_POW_BLOCK_DIFFICULTY: uint64
    TARGET_SECONDS_TO_MERGE: uint64
    MIN_GENESIS_TIME: uint64


# Mainnet numbers
config = Configuration(
    # 12 seconds
    SECONDS_PER_SLOT=uint64(12),
    # 14 (estimate from Eth1 mainnet)
    SECONDS_PER_ETH1_BLOCK=uint64(14),
    # 2**6 (= 64) epochs ~6.8 hours
    EPOCHS_PER_ETH1_VOTING_PERIOD=uint64(64),
    # 2**5 (= 32) slots 6.4 minutes
    SLOTS_PER_EPOCH=uint64(32),
    # 2**11 (= 2,048) Eth1 blocks ~8 hours
    ETH1_FOLLOW_DISTANCE=uint64(2048),
    # TBD, 2**32 is a placeholder. Merge transition approach is in active R&D.
    MIN_ANCHOR_POW_BLOCK_DIFFICULTY=uint64(4294967296),
    # 7 * 60*60*24 = 7 days
    TARGET_SECONDS_TO_MERGE=uint64(604800),
    # Dec 1, 2020, 12pm UTC
    MIN_GENESIS_TIME = uint64(1606824000),
)
