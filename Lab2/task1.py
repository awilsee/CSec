import hashlib
import os

from Crypto.Cipher import AES


aes_bytes = 16
#p = 37
#g = 5
p = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
g = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)


def add_pkcs7(input):
    num_bytes = aes_bytes - (len(input) % aes_bytes)
    fil_bytes = bytes()
    for x in range(num_bytes):
        fil_bytes += bytes([num_bytes])
    input += fil_bytes
    return input


def remove_pkcs7(input):
    pad_byte = input[len(input) - 1]
    return input[:len(input) - pad_byte]


if __name__ == '__main__':
    privA = 6
    privB = 15

    shared_a = (g ** privA) % p
    shared_b = (g ** privB) % p

    calc_shared_secA = (shared_b ** privA) % p
    calc_shared_secB = (shared_a ** privB) % p

    hash_a = hashlib.sha256("{}".format(int(calc_shared_secA)).encode()).digest()
    hash_b = hashlib.sha256("{}".format(int(calc_shared_secB)).encode()).digest()

    print(hash_a)
    print(hash_b)

    m_a = b"Hi Bob!"
    m_b = b"Hi Alice!"

    m_a = add_pkcs7(m_a)
    m_b = add_pkcs7(m_b)

    #encrypting
    init_iv = os.urandom(16)
    cipher_a = AES.new(hash_a[:16], AES.MODE_CBC, init_iv)
    crypt_a = cipher_a.encrypt(m_a)

    cipher_b = AES.new(hash_b[:16], AES.MODE_CBC, init_iv)
    crypt_b = cipher_b.encrypt(m_b)

    #decrypting
    cipher_a = AES.new(hash_a[:16], AES.MODE_CBC, init_iv)
    msg_a = cipher_a.decrypt(crypt_b)

    cipher_b = AES.new(hash_b[:16], AES.MODE_CBC, init_iv)
    msg_b = cipher_b.decrypt(crypt_a)

    print(remove_pkcs7(msg_a))
    print(remove_pkcs7(msg_b))



