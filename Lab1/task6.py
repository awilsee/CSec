import base64
import binascii
import os
import urllib.parse

from task5 import add_pkcs7
from task5 import encrypt_cbc
from task5 import decrypt_cbc

aes_bytes = 16

init_iv = os.urandom(aes_bytes)


def submit(data):
    url = "userid=321;userdata=" + data + ";session-id=31337"
    url = urllib.parse.quote(url, safe="\' ',")
    url = add_pkcs7(bytes(url, 'utf-8'))
    return encrypt_cbc(url, init_iv)


def verify(data):
    url = decrypt_cbc(data, init_iv)
    if -1 == url.decode().find(";admin=true;"):
        return False
    else:
        return True


if __name__ == '__main__':
    txt = "You're the man now, dog"
    txt = input("Enter string: ")
    print("Entered String: " + txt)
    enc_url = submit(txt)
    print()

    if verify(enc_url):
        print("Congrats you're admin!")
    else:
        print("You're NOT admin with your string!")
