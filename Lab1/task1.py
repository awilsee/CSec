import binascii
from itertools import cycle

from Crypto.Cipher import XOR


def xorfunc(txtCipher, txt):
    if len(txtCipher) != len(txt):
        raise NameError('The two strings hasn\'t equal lenght!')
    return bytes([a ^ b for (a, b) in zip(txtCipher, cycle(txt))])
    #cipher = XOR.new(txtCipher) #only 1 to 32 bytes long
    #return cipher.encrypt(txt)


if __name__ == '__main__':
    txtDarlin = "Darlin dont you go"
    txtHair = "and cut your hair!"


    print("txt:", txtDarlin)
    print("cipher:", txtHair)

    #print("\nencrypted: ", binascii.hexlify(xorfunc(txtHair, txtDarlin)))
    print("\nencrypted: ", '[{}]'.format(' ' .join(hex(x) for x in xorfunc(bytes(txtHair, 'utf-8'), bytes(txtDarlin, 'utf-8')))))
