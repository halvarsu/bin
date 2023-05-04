#!/bask/homes/p/ppwg9728/miniconda3/bin/python

import pandas as pd
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-o", "--out", default='train_stats.csv')
    return parser.parse_args()

def main():
    args = get_args()
    with open(args.file) as infile:
        lines = [line.strip() for line in infile.readlines()]
        columns = ['step', 'energy', 'variance', 'pmove', 'num_outliers']
        data = []
        for line in lines:
            if " Step " in line:
                values = line[line.find("Step"):].split()
                step = int(values[1][:-1])
                energy = float(values[2])
                variance = float(values[4].split('=')[1])
                pmove = float(values[6].split('=')[1][:-1])
                outliers = int(values[7].split('=')[1])
                # print(step, energy, variance, pmove, outliers)
                data.append([step, energy, variance, pmove, outliers])
        data = pd.DataFrame(data, columns = columns)
        data.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()

