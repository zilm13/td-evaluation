import csv


ETH2_DATA_PATH = "./eth1votes.csv"
HASH_DATA_PATH = "./hash.csv"
OUTPUT_DATA_PATH = "./eth1_votes.csv"


def main():
    hash_data = dict()
    with open(HASH_DATA_PATH) as rp:
        reader = csv.reader(rp, delimiter=",", quotechar='"')
        for row in reader:
            hash_data[row[1]] = int(row[0])
    print("All hash data readed, writing!")
    with open(OUTPUT_DATA_PATH, "wt") as wp:
        writer = csv.writer(wp, delimiter=",")
        # write header
        writer.writerow(["slot", "eth1_block_hash", "eth1_block_number"])
        with open(ETH2_DATA_PATH) as rp:
            reader = csv.reader(rp, delimiter=",", quotechar='"')
            for row in reader:
                writer.writerow((row[0], row[1], hash_data.get(row[1], "None")))


main()
