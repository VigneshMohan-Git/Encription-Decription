from EncDec import generate_new_key_pair, path_leaf, encrypt_blob, decrypt_blob, copyfile

import zlib
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from pathlib import Path

path_to_key = '/home/folder/'
key_savepath = '/home/folder/'
#generate_new_key_pair(path_to_key)

private_key = '/home/folder/private.pem'
public_key = '/home/folder/public.pem'

unencrypted_file = '/home/folder/DBData.csv'
encrypted_file_path = "/home/folder/DBData_encrypted"
src = "/home/folder/DBData_encrypted"
dec = "/home/folder/DBData_encrypted"

# -- Encrytion
filename = path_leaf(unencrypted_file)
encrypt_blob(unencrypted_file, public_key, key_savepath, filename)

# -- File Transfer
copyfile(src, dec)

# -- Decrytion
decrypt_blob(encrypted_file_path, private_key, path_to_key, filename)