import binascii
import os

from task1 import xorfunc

pic1 = "./cp-logo.bmp"
pic1Enc = "./cp-logo-enc.bmp"
pic2 = "./mustang.bmp"
pic2Enc = "./mustang-enc.bmp"
pic3Enc = "./random-enc.bmp"
picDec = "./pic-dec.bmp"

fileLength = len(open(pic1, "rb").read())


def write_bmp_file(filename, input):
    byteEnc = open("./cp-logo.bmp", "rb").read(54)
    byteEnc += input[54:]
    open(filename, "wb").write(byteEnc)


def encryptBMPFile(picFilePath, picEncFilePath, cipher=os.urandom(fileLength)):
    file = open(picFilePath, "rb").read()
    print("file {} has {:d} characters".format(picFilePath, len(file)))

    txtEnc = xorfunc(cipher, file)
    # print("\nencryptedHEX: ", '[{}]'.format(' ' .join(hex(x) for x in txtEnc)))

    write_bmp_file(picEncFilePath, txtEnc)

    txtDec = xorfunc(cipher, txtEnc)

    open(picDec, "wb").write(txtDec)


def generateRndBMPFile(picEncFilePath, cipher=os.urandom(fileLength)):
    write_bmp_file(picEncFilePath, cipher)


if __name__ == '__main__':
    encryptBMPFile(pic1, pic1Enc)
    encryptBMPFile(pic2, pic2Enc)
    generateRndBMPFile(pic3Enc)
