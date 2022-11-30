from EncDec import generate_new_key_pair, path_leaf, encrypt_blob, decrypt_blob, copyfile

import zlib
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from pathlib import Path

path_to_key = '/home/mclen/dex/sql_files/'
key_savepath = '/home/mclen/dex/sql_files/'
#generate_new_key_pair(path_to_key)

private_key = '/home/mclen/dex/sql_files/private.pem'
public_key = '/home/mclen/dex/sql_files/public.pem'

unencrypted_file = '/home/mclen/dex/sql_files/DBData.csv'
encrypted_file_path = "/home/mclen/dex/sql_files/DBData_encrypted"
src = "/home/mclen/dex/sql_files/DBData_encrypted"
dec = "/home/mclen/dex/sql_files/DBData_encrypted"

# -- Encrytion
filename = path_leaf(unencrypted_file)
encrypt_blob(unencrypted_file, public_key, key_savepath, filename)

# -- File Transfer
copyfile(src, dec)

# -- Decrytion
decrypt_blob(encrypted_file_path, private_key, path_to_key, filename)