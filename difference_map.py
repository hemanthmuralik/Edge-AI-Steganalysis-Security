import argparse
import numpy as np
from PIL import Image, ImageOps

def main(orig_path, stego_path, out_path):
    o = Image.open(orig_path).convert('RGB')
    s = Image.open(stego_path).convert('RGB').resize(o.size)
    oa = np.array(o).astype(int)
    sa = np.array(s).astype(int)
    diff = np.abs(oa - sa).astype('uint8')
    # amplify difference for visibility
    diff = (diff * 8).clip(0,255).astype('uint8')
    Image.fromarray(diff).save(out_path)
    print('Wrote difference map to', out_path)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--orig', required=True, help='original cover image')
    p.add_argument('--stego', required=True, help='stego image')
    p.add_argument('--out', required=True, help='output diff image path')
    args = p.parse_args()
    main(args.orig, args.stego, args.out)
