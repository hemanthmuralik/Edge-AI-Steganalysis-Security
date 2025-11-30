"""Generate a dataset using CIFAR10 images. For each clean image, create a stego image
by embedding a short random payload using LSB on red channel.
"""
import os, argparse, numpy as np
from tensorflow.keras.datasets import cifar10
from PIL import Image
from utils import embed_lsb

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def main(outdir='./data', num=2000):
    (x_train, _), (x_test, _) = cifar10.load_data()
    X = np.concatenate([x_train, x_test], axis=0)
    X = X.astype('uint8')
    ensure_dir(os.path.join(outdir, 'clean'))
    ensure_dir(os.path.join(outdir, 'stego'))
    count = 0
    for i,img in enumerate(X):
        if count >= num:
            break
        img = img  # 32x32x3
        clean_path = os.path.join(outdir, 'clean', f'{count:04d}.png')
        Image.fromarray(img).save(clean_path)
        # create random small payload
        payload = os.urandom(12)  # 12 bytes -> 96 bits, small
        stego_arr = embed_lsb(img, payload)
        stego_path = os.path.join(outdir, 'stego', f'{count:04d}.png')
        Image.fromarray(stego_arr).save(stego_path)
        count += 1
    print(f'Wrote {count} clean + stego images into {outdir}')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--outdir', default='./data')
    p.add_argument('--num', type=int, default=2000, help='total number of images (clean and stego)')
    args = p.parse_args()
    main(args.outdir, args.num)
