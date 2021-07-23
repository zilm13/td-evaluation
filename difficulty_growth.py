# from evaluate_target import compute_target_delay
from evaluate import compute_transition_total_difficulty, PowBlock

TOTAL_DIFFICULTY =  27886712656263580414632
MAX_DIFFICULTY = 6856186631660169
INITIAL_DIFFICULTY = MAX_DIFFICULTY // 2
DIFFICULTY_BOUND_DIVISOR = 2048
MINIMUM_DIFFICULTY = 131072
EXP_DIFFICULTY_PERIOD = 100000
BOMB_BLOCK = 11000000
START_BLOCK = 13000000


def get_explosion(block_number):
    period_count = max(0, (block_number - BOMB_BLOCK)) // EXP_DIFFICULTY_PERIOD
    return period_count - 2


def calc_difficulty(parent_difficulty, block_number):
    quotient = parent_difficulty // DIFFICULTY_BOUND_DIVISOR
    sign = 2  # maximum possible sign, 0 delay with uncles
    from_parent = parent_difficulty + (quotient * sign)
    difficulty = max(MINIMUM_DIFFICULTY, from_parent)
    explosion = get_explosion(block_number)
    if explosion >= 0:
        difficulty = max(MINIMUM_DIFFICULTY, difficulty + pow(2, explosion))

    return min(difficulty, MAX_DIFFICULTY)


def main():
    anchor_block = PowBlock(difficulty=INITIAL_DIFFICULTY, total_difficulty=TOTAL_DIFFICULTY)
    transition_total_difficulty = compute_transition_total_difficulty(anchor_block)
    block = START_BLOCK
    difficulty = INITIAL_DIFFICULTY
    total_difficulty = TOTAL_DIFFICULTY
    while True:
        block += 1
        difficulty = calc_difficulty(difficulty, block)
        total_difficulty += difficulty
        if total_difficulty > transition_total_difficulty:
            print("Transition block #{} difficulty {}".format(block, difficulty))
            break


main()
