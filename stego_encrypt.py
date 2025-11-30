import argparse, getpass
from PIL import Image
import numpy as np
from utils.aes_utils import derive_key, encrypt_aes256_gcm
from utils.lsb_utils import embed_bytes_in_image, load_image, save_image

def main(in_path, out_path, text=None, infile=None):
    # load image
    img = load_image(in_path)
    # read payload
    if text is not None:
        payload = text.encode('utf-8')
    else:
        with open(infile, 'rb') as f:
            payload = f.read()
    # ask passphrase and derive key+salt
    passphrase = getpass.getpass('Passphrase (will derive AES-256 key): ')
    key, salt = derive_key(passphrase)
    # encrypt with AES-GCM
    nonce, ciphertext, tag = encrypt_aes256_gcm(key, payload)
    # prepare blob = salt(16) + nonce(12) + tag(16) + ciphertext
    blob = salt + nonce + tag + ciphertext
    # embed into image
    stego = embed_bytes_in_image(img, blob)
    save_image(stego, out_path)
    print('Wrote stego image to', out_path)
    print('Note: keep the passphrase to decrypt. Salt is stored inside the image.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Encrypt payload (AES-256-GCM) and embed into image LSB')
    p.add_argument('--in', dest='in_path', required=True, help='input cover image (PNG recommended)')
    p.add_argument('--out', dest='out_path', required=True, help='output stego image path')
    p.add_argument('--text', dest='text', help='text payload to embed (mutually exclusive with --file)')
    p.add_argument('--file', dest='infile', help='file to embed as payload')
    args = p.parse_args()
    if args.text is None and args.infile is None:
        print('Provide --text or --file')
    else:
        main(args.in_path, args.out_path, text=args.text, infile=args.infile)
