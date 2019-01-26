import os
import urllib.parse

from Crypto.Cipher import AES

from task5 import add_pkcs7
from tasks import encrypt_cbc

txtfilePath = "./txtFile"
pic1 = "./cp-logo.bmp"
pic2 = "./mustang.bmp"

ending_ecb = "-enc-ecb.bmp"
ending_cbc = "-enc-cbc.bmp"

aes_bytes = 16
cipher_key = os.urandom(aes_bytes)
aes_prim = AES.new(cipher_key)

init_iv = os.urandom(aes_bytes)


def submit(data):
    url = "userid=321;userdata=" + data + ";session-id=31337"
    url = urllib.parse.quote(url, safe="\' ',")
    print("1: " + url)
    url = add_pkcs7(url)
    print("2: " + url)
    return encrypt_cbc(url, init_iv)


def verify(data):
    url = "dd"#decrypt_cbc(data)
    if -1 == url.find(";admin=true;"):
        return False
    else:
        return True


if __name__ == '__main__':
    txt = "You're the man now, dog"
    print("Entered String: " + txt)
    enc_url = submit(txt)
    if verify(enc_url):
        print("Congrats you're admin!")
    else:
        print("You're not admin with your string!")



    '''
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
'''