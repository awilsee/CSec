import os

from task5 import add_pkcs7
from task5 import encrypt_cbc
from task5 import decrypt_cbc

aes_bytes = 16
init_iv = os.urandom(aes_bytes)


def submit(data):
    url = "userid=321;userdata=" + data + ";session-id=31337"
    for i in range(len(url)):
        if url[i] == ";" or url[i] == "=":
            url = url.replace(url[i], "*")
    #url = urllib.parse.quote(url, safe="\' ',")

    url_bytes = add_pkcs7(bytes(url, 'utf-8'))
    return encrypt_cbc(url_bytes, init_iv)


def verify(data):
    url = decrypt_cbc(data, init_iv)
    #print(url)
    if -1 == url.decode('utf-8', 'ignore').find(";admin=true;"):
        return False
    else:
        return True


# modify cipher block to modify following plaintext
def modify_block(enc_data):
    cipher_list = []
    i = 0
    # get blocks
    while i * 16 < len(enc_url):
        cipher_list.append(enc_url[i * 16: 16 + (i * 16)])
        i += 1

    # modify cipher block before actual plaintext block
    block_to_modify = cipher_list[0]
    block_list = list(block_to_modify)
    block_list[4] ^= ord("*") ^ ord(";")
    block_list[10] ^= ord("*") ^ ord("=")
    block_list[15] ^= ord("*") ^ ord(";")
    cipher_list[0] = bytes(block_list)
    return b''.join(cipher_list)


if __name__ == '__main__':
    #txt = "You're the man now, dog"
    txt = ";admin=true"
    #txt = input("Enter string: ")
    print("Entered String: " + txt)

    #submit and encrypt input string
    enc_url = submit(txt)

    #modify block
    enc_url = modify_block(enc_url)

    #call verify
    if verify(enc_url):
        print("\nCongrats! You're admin!")
    else:
        print("\nYou're NOT admin with your string!")

