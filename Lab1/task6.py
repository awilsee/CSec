import os
import urllib.parse

from task5 import add_pkcs7
from tasks import encrypt_cbc

aes_bytes = 16

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
