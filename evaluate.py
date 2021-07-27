import csv
from util import compute_transition_total_difficulty, PowBlock


DIFFICULTY_DATA_PATH = "./blocks_4_mainnet.csv"
RESULT_OUTPUT_DATA_PATH = "./result.csv"


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
