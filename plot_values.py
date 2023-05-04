#!/bask/homes/p/ppwg9728/miniconda3/bin/python
import sys
import pandas as pd
import numpy as np
import asciichartpy
import argparse
import shutil
import json
import matplotlib.pyplot as plt

TERMINAL_SIZE=shutil.get_terminal_size((80, 20))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    parser.add_argument("-W",
	    "--width",
	    type=int,
	    default=TERMINAL_SIZE.columns - 12,
	    help="width")
    parser.add_argument("-H",
	    "--height",
	    type=int,
	    default=TERMINAL_SIZE.lines - 5,
	    help="height")
    parser.add_argument("-b",
	    "--baseline",
	    type=float,
	    help="value to subtract from data",
	    default=0)
    parser.add_argument("-l", "--log", action="store_true", help="do the log")
    parser.add_argument("-m", "--medfilt", action="store_true", help="do the median filter")
    parser.add_argument("--save_matplotlib", action="store_true", help="save matplotlib file")
    parser.add_argument("-v", "--variance", action="store_true", help="plot variance")
    parser.add_argument("--mpl_title", default="")

    args = parser.parse_args()
    if not args.file.name.endswith(".csv"):
        raise ValueError("file must be csv")
    return args

def tenperc_medfilt(y):
  """take the median of last 10 percent of values at each point"""
  y = np.asarray(y)
  out = [y[0]]
  for i in range(1, len(y)):
    nmed = max(i // 10, 1)
    out.append(np.median(y[i-nmed:i]))
  return out


def load(args):
    return pd.read_csv(args.file)


def save_matplotlib(energy, args):
    if args.log:
        plt.loglog(energy - args.baseline)
    else:
        plt.plot(energy - args.baseline)
    plt.title(args.mpl_title)
    plt.ylabel("Energy - baseline")
    plt.xlabel("step")
    figname = "training_data.png"
    print(f"Saving figure {figname}")
    plt.savefig(figname)


def main():
    args = get_args()
    df = load(args)

    if args.variance:
        var = df.variance.values
    else:
        var = df.energy.values
    if args.medfilt:
        var = np.array(tenperc_medfilt(var))


    plot_kwargs = {"height": args.height}
    print("Plotting {}{} energies".format("log-log of " if args.log else "", df.shape[0]))
    if args.log:
        baseline = args.baseline or (np.mean(var[-max(var.size//100, 1):]) if not args.variance else 0)
        y = np.log10(np.abs(var - baseline))
        n = y.size

        num_x_vals = args.width
        ind = np.logspace(np.log10(2), np.log10(n), num_x_vals, dtype=int) - 1
        print(asciichartpy.plot(y[ind], plot_kwargs))

    else:
        y = var - args.baseline
        n = y.size
        nsteps = max(1, n // args.width)

        print(asciichartpy.plot(y[::nsteps], plot_kwargs))
    if args.save_matplotlib:
        save_matplotlib(var, args)

if __name__ == "__main__":
    main()
