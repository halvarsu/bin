#!/bask/homes/p/ppwg9728/miniconda3/bin/python

import glob
import sys

folders = sys.argv[1:] or ['.']

for folder in folders:
    f = sorted(glob.glob("/".join((folder, "*.npz"))))[-1]
    print(f, end=' ')
