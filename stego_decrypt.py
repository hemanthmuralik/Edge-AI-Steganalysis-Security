import argparse, getpass
from utils.lsb_utils import load_image, extract_bytes_from_image
from utils.aes_utils import derive_key, decrypt_aes256_gcm

def main(in_path, out_path=None):
    img = load_image(in_path)
    blob = extract_bytes_from_image(img)
    # parse blob: salt(16) + nonce(12) + tag(16) + ciphertext
    if len(blob) < 44:
        raise ValueError('Blob too small to contain salt+nonce+tag')
    salt = blob[:16]
    nonce = blob[16:28]
    tag = blob[28:44]
    ciphertext = blob[44:]
    passphrase = getpass.getpass('Passphrase (to derive AES-256 key): ')
    key, _ = derive_key(passphrase, salt=salt)
    plaintext = decrypt_aes256_gcm(key, nonce, ciphertext, tag)
    if out_path:
        with open(out_path, 'wb') as f:
            f.write(plaintext)
        print('Wrote extracted payload to', out_path)
    else:
        try:
            print('Payload (as text):')
            print(plaintext.decode('utf-8'))
        except Exception:
            print('Payload is binary; use --out to write to file.')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='in_path', required=True, help='input stego image')
    p.add_argument('--out', dest='out_path', help='output file for extracted payload (optional)')
    args = p.parse_args()
    main(args.in_path, args.out_path)
