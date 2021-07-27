import csv
from sortedcontainers import SortedList
from util import compute_target_delay

INPUT_DATA_PATH = "./result.csv"
OUTPUT_DATA_PATH = "./result_target.csv"


class ReadRecord(object):
    def __init__(self, block, difficulty, total_difficulty, transition_total_difficulty, timestamp):
        self.block = block
        self.difficulty = difficulty
        self.total_difficulty = total_difficulty
        self.transition_total_difficulty = transition_total_difficulty
        self.timestamp = timestamp

    def _cmp_key(self):
        return self.transition_total_difficulty

    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()

    def __lt__(self, other):
        return self._cmp_key() < other._cmp_key()


class WriteRecord(object):
    def __init__(self, block, other):
        self.block = block
        self.other = other

    def _cmp_key(self):
        return self.block

    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()

    def __lt__(self, other):
        return self._cmp_key() < other._cmp_key()


def main():
    sl = SortedList()
    buffer = SortedList()
    next_block = 0
    target_delay = compute_target_delay()
    with open(OUTPUT_DATA_PATH, "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        # write header
        writer.writerow(["block", "difficulty", "total_difficulty", "transition_total_difficulty",
                         "transition_real_block", "transition_real_timestamp", "transition_delta_blocks",
                         "timestamp"])
        with open(INPUT_DATA_PATH) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            next(reader, None)  # skip the headers
            for row in reader:
                record = ReadRecord(int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]))
                sl.add(record)
                flag = True
                while flag:
                    if len(sl) == 0:
                        break
                    lowest_record = sl[0]
                    if record.total_difficulty >= lowest_record.transition_total_difficulty:
                        sl.pop(0)
                        buffer.add(WriteRecord(lowest_record.block, (lowest_record.difficulty,
                                                                     lowest_record.total_difficulty,
                                                                     lowest_record.transition_total_difficulty,
                                                                     record.block,
                                                                     record.timestamp,
                                                                     record.block - lowest_record.block - target_delay,
                                                                     lowest_record.timestamp)))
                        while len(buffer) > 0 and buffer[0].block <= next_block:
                            writer.writerow((buffer[0].block, *buffer[0].other))
                            buffer.pop(0)
                            next_block += 1
                    else:
                        flag = False


main()
