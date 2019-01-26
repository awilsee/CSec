import os
from Crypto.Cipher import AES

from task3 import write_bmp_file

txtfilePath = "./txtFile"
txtfilePathEnc = "./txtFile-enc-t5"
pic1 = "./cp-logo.bmp"
pic1Enc = "./cp-logo-enc-t5.bmp"
pic2 = "./mustang.bmp"
pic2Enc = "./mustang-enc-t5.bmp"
picDec = "./pic-dec.bmp"

aes_bytes = 16
aes_prim = AES.new(os.urandom(aes_bytes))


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

    file = add_pkcs7(file, aes_bytes - (file_length % aes_bytes))

    x = 0
    file_enc = bytes()
    while x < len(file) / aes_bytes:
        file_enc += aes_prim.encrypt(file[x:(x + aes_bytes)])
        x += 1
    return file_enc

def encrypt_cbc(file_path, key):
    print("nothing")


if __name__ == '__main__':
    enc_txt = encrypt_ecb(txtfilePath)
    open(txtfilePathEnc, "wb").write(enc_txt)

    enc_bytes = encrypt_ecb(pic1)
    write_bmp_file(pic1Enc, enc_bytes)

    enc_bytes = encrypt_ecb(pic2)
    write_bmp_file(pic2Enc, enc_bytes)


