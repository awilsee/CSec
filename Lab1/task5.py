import os
from Crypto.Cipher import AES

from task3 import write_bmp_file
from task1 import xorfunc

txtfilePath = "./txtFile"
pic1 = "./cp-logo.bmp"
pic2 = "./mustang.bmp"

ending_ecb = "-enc-ecb.bmp"
ending_cbc = "-enc-cbc.bmp"

aes_bytes = 16
cipher_key = os.urandom(aes_bytes)
aes_prim = AES.new(cipher_key)


def add_pkcs7(input):
    num_bytes = aes_bytes - (len(input) % aes_bytes)
    fil_bytes = bytes()
    for x in range(num_bytes):
        fil_bytes += bytes([num_bytes])
    input += fil_bytes
    return input


def get_padded_file(file_path):
    file = open(file_path, "rb").read()
    print("file {} has {:d} characters".format(file_path, len(file)))

    # padding
    return add_pkcs7(file)


def encrypt_ecb(data):
    x = 0
    file_enc = bytes()
    while x < len(data) / aes_bytes:
        file_enc += aes_prim.encrypt(data[x * aes_bytes:((x + 1) * aes_bytes)])
        x += 1
    return file_enc


def encrypt_ecb_file(file_path):
    return encrypt_ecb(get_padded_file(file_path))


def encrypt_cbc(data, init_iv):
    x = 0
    file_enc = bytes()
    while x < len(data) / aes_bytes:
        if 0 == x:
            xor_bytes = xorfunc(init_iv, data[x * aes_bytes:((x + 1) * aes_bytes)])
        else:
            xor_bytes = xorfunc(file_enc[(x - 1) * aes_bytes:(x * aes_bytes)], data[x * aes_bytes:((x + 1) * aes_bytes)])
        file_enc += aes_prim.encrypt(xor_bytes)
        x += 1
    return file_enc


def encrypt_cbc_file(file_path, init_iv):
    return encrypt_cbc(get_padded_file(file_path), init_iv)



if __name__ == '__main__':
    enc_txt = encrypt_ecb_file(txtfilePath)
    open(txtfilePath + ending_ecb[:8], "wb").write(enc_txt)

    #test decyrpt ecb
    cipher = AES.new(cipher_key, AES.MODE_ECB)
    plaintext = cipher.decrypt(enc_txt)
    print(plaintext)

    enc_bytes = encrypt_ecb_file(pic1)
    write_bmp_file(pic1 + ending_ecb, enc_bytes)

    enc_bytes = encrypt_ecb_file(pic2)
    write_bmp_file(pic2 + ending_ecb, enc_bytes)

    init_iv = os.urandom(aes_bytes)
    enc_txt = encrypt_cbc_file(txtfilePath, init_iv)
    open(txtfilePath + ending_cbc[:8], "wb").write(enc_txt)

    #test decyrpt cbc
    cipher = AES.new(cipher_key, AES.MODE_CBC, init_iv)
    plaintext = cipher.decrypt(enc_txt)
    print(plaintext)

    enc_bytes = encrypt_cbc_file(pic1, init_iv)
    write_bmp_file(pic1 + ending_cbc, enc_bytes)

    enc_bytes = encrypt_cbc_file(pic2, init_iv)
    write_bmp_file(pic2 + ending_cbc, enc_bytes)
