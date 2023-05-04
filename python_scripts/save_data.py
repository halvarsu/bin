#!/p/project/pra135/halvard/envs/ecp/ecp/bin/python3

from ferminet.checkpoint import restore
import numpy as np

import glob

def save_data(restore_filename):
    # *name, ext = restore_filename.split(".")
    out_filename = restore_filename + "_data" #".".join(name + [ext + "_data",])

    with open(restore_filename, 'rb') as f:
      ckpt_data = np.load(f, allow_pickle=True)
      t = ckpt_data['t'].tolist()  # Return the iterations completed.
      data = ckpt_data['data']
    with open(out_filename, 'wb') as f:
      print(f"saving to {out_filename}")
      np.savez(f, t=t, data=data)
    return out_filename

if __name__ == "__main__":
    import sys
    files = sys.argv[1:]
    if not files:
        print("no files")
    for f in files:
        save_data(f)
