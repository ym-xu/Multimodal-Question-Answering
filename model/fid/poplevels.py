import argparse
import json
import csv
import math

def main(datadir, levels, savedir):

    with open(datadir, newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        data = list(reader)

    print(data)

    pop_dict = {i[0]: i[1] for i in data}

    sorted_data = sorted(pop_dict.items(), key=lambda x: int(x[1]))
    group_size = math.ceil(len(sorted_data) / levels)

    poplevels = {}

    for i in range(0, len(sorted_data), group_size):
        group = sorted_data[i:i+group_size]
        for key, value in group:
            poplevels[key] = i // group_size

    with open(savedir, "w") as f:
        json.dump(poplevels, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a demo script.')
    parser.add_argument('--datadir', type = str, default = 'NQ')
    parser.add_argument('--levels', type = int, default = 8)
    parser.add_argument('--savedir', type = str, default = 'obj')
    args = parser.parse_args()
    main(args.datadir, args.levels, args.savedir)