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


def add_pkcs7(input, num_bytes):
    fil_bytes = bytes()
    for x in range(num_bytes):
        fil_bytes += bytes([num_bytes])
    input += fil_bytes
    return input


def encrypt_ecb(file_path):
    file = open(file_path, "rb").read()
    file_length = len(file)
    print("file {} has {:d} characters".format(file_path, file_length))

    #padding
    file = add_pkcs7(file, aes_bytes - (file_length % aes_bytes))

    x = 0
    file_enc = bytes()
    while x < len(file) / aes_bytes:
        file_enc += aes_prim.encrypt(file[x * aes_bytes:((x + 1) * aes_bytes)])
        x += 1
    return file_enc


def encrypt_cbc(file_path, init_iv):
    file = open(file_path, "rb").read()
    file_length = len(file)
    print("file {} has {:d} characters".format(file_path, file_length))

    #padding
    file = add_pkcs7(file, aes_bytes - (file_length % aes_bytes))

    x = 0
    file_enc = bytes()
    while x < len(file) / aes_bytes:
        if 0 == x:
            xor_bytes = xorfunc(init_iv, file[x * aes_bytes:((x + 1) * aes_bytes)])
        else:
            xor_bytes = xorfunc(file_enc[(x - 1) * aes_bytes:(x * aes_bytes)], file[x * aes_bytes:((x + 1) * aes_bytes)])
        file_enc += aes_prim.encrypt(xor_bytes)
        x += 1
    return file_enc


if __name__ == '__main__':
    enc_txt = encrypt_ecb(txtfilePath)
    open(txtfilePath + ending_ecb[:8], "wb").write(enc_txt)

    #test decyrpt ecb
    cipher = AES.new(cipher_key, AES.MODE_ECB)
    plaintext = cipher.decrypt(enc_txt)
    print(plaintext)

    enc_bytes = encrypt_ecb(pic1)
    write_bmp_file(pic1 + ending_ecb, enc_bytes)

    enc_bytes = encrypt_ecb(pic2)
    write_bmp_file(pic2 + ending_ecb, enc_bytes)

    init_iv = os.urandom(aes_bytes)
    enc_txt = encrypt_cbc(txtfilePath, init_iv)
    open(txtfilePath + ending_cbc[:8], "wb").write(enc_txt)

    #test decyrpt cbc
    cipher = AES.new(cipher_key, AES.MODE_CBC, init_iv)
    plaintext = cipher.decrypt(enc_txt)
    print(plaintext)

    enc_bytes = encrypt_cbc(pic1, init_iv)
    write_bmp_file(pic1 + ending_cbc, enc_bytes)

    enc_bytes = encrypt_cbc(pic2, init_iv)
    write_bmp_file(pic2 + ending_cbc, enc_bytes)
