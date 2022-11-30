def generate_new_key_pair(path_to_key):
    
    new_key = RSA.generate(4096, e=65537)
    private_key = new_key.exportKey("PEM")
    public_key = new_key.publickey().exportKey("PEM")

    private_key_path = Path(path_to_key + 'private.pem')
    private_key_path.touch(mode=0o600)
    private_key_path.write_bytes(private_key)

    public_key_path = Path(path_to_key + 'public.pem')
    public_key_path.touch(mode=0o664)
    public_key_path.write_bytes(public_key)
    print("Key Generated")

    
def path_leaf(filepath):
    import os
    file_path = filepath
    file_name = os.path.basename(file_path)
    index_of_dot = file_name.index('.')
    file_name_without_extension = file_name[:index_of_dot]
    return file_name_without_extension
    
    
# Our Encryption Function
def encrypt_blob(unencrypted_file, public_key, file_save_path, filename):
    
    unencrypted_path = Path(unencrypted_file)
    #unencrypted_sufix = unencrypted_path.with_suffix('.dat')
    unencrypted_file_bytes = unencrypted_path.read_bytes()
    public_key=Path(public_key)
    
    with open(public_key, "rb") as k:
        rsa_key = RSA.importKey(k.read())
        rsa_key = PKCS1_OAEP.new(rsa_key)
    
    blob = zlib.compress(unencrypted_file_bytes)

    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted = bytearray()

    while not end_loop:
        chunk = blob[offset:offset + chunk_size]

        if len(chunk) % chunk_size != 0:
            end_loop = True
            # chunk += b" " * (chunk_size - len(chunk))
            chunk += bytes(chunk_size - len(chunk))
        encrypted += rsa_key.encrypt(chunk)

        offset += chunk_size

        with open(file_save_path + filename + "_encrypted", 'wb') as encrypted_file:
            encrypted_file.write(base64.b64encode(encrypted))
            
    print("File Encrypted")
    return base64.b64encode(encrypted)


# Decryption Function
def decrypt_blob(encrypted_file_path, private_key, file_save_path, filename):
    encrypted_file_path=Path(encrypted_file_path)
    private_key = Path(private_key)
    
    with open(private_key, "rb") as k:
        rsakey = RSA.importKey(k.read())
        rsakey = PKCS1_OAEP.new(rsakey)

    with open(encrypted_file_path) as f:
        data = f.read()
    
    encrypted_blob = base64.b64decode(data)

    chunk_size = 512
    offset = 0
    decrypted = bytearray()

    while offset < len(encrypted_blob):
        chunk = encrypted_blob[offset: offset + chunk_size]
        decrypted += rsakey.decrypt(chunk)
        offset += chunk_size

    data = zlib.decompress(decrypted)
    with open(file_save_path + filename + '.csv', 'wb') as decrypted_file:
        decrypted_file.write(data)
    
    return print("File Decrypted & saved:", file_save_path)

# Local filecopy
def copyfile(src, dec):
    import shutil
    shutil.copy2(src, dec)
    print("File Copied",src,dec)