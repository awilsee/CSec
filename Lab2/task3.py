# http://inventwithpython.com/hacking (BSD Licensed)

import PrimesRabinMiller as prm

e = 65537
KEY_SIZE = 1024 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def gen_prime_key(key_size):
    #Creating two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = prm.generate_prime_number(key_size)
    print('Generating q prime...')
    q = prm.generate_prime_number(key_size)
    n = p * q

    #Calculate d, the mod inverse of e, e is static
    print('Calculating d that is mod inverse of e...')
    d = findModInverse(e, (p - 1) * (q - 1))
    public_k = (n, e)
    private_k = (n, d)
    print('Public key :', public_k)
    print('Private key:', private_k)

    return public_k, private_k


def get_blocks_from_string(msg, blockSize=KEY_SIZE // 8):
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blockSize is set to) string characters.
    msgBytes = msg.encode('ascii') # convert the string to bytes
    blockInts = []
    for blockStart in range(0, len(msgBytes), blockSize):
        # Calculate the block integer for this block of text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(msgBytes))):
            blockInt += msgBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def get_string_from_blocks(blockInts, msgLen, blockSize=KEY_SIZE // 8):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < msgLen:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encrypt_msg(msg, pub_key):
    encrypted_blocks = []

    for blocks in get_blocks_from_string(msg):
        # c = plain ^ e mod n
        encrypted_blocks.append(pow(blocks, pub_key[1], pub_key[0]))
    return encrypted_blocks


def decrypt_msg(block_msg, priv_key, msgLen):
    decrypt_blocks = []
    for blocks in block_msg:
        # plain = c ^ d mod n
        decrypt_blocks.append(pow(blocks, priv_key[1], priv_key[0]))
    return get_string_from_blocks(decrypt_blocks, msgLen)


if __name__ == '__main__':

    public_k, private_k = gen_prime_key(KEY_SIZE)

    msg1 = "Hello World!"
    msg2 = "This is a string which includes more than 128 Bytes. It is used to test if the block building also works if you have more than block_size Bytes."

    enc_msg = encrypt_msg(msg2, public_k)

    dec_msg = decrypt_msg(enc_msg, private_k, len(msg2))

    print(dec_msg)
