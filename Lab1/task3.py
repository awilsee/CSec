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
fileHeader = open(pic1, "rb").read(54)


def encryptBMPFile(picFilePath, picEncFilePath, cipher=os.urandom(fileLength)):
    file = open(picFilePath, "rb").read()
    print("file {} has {:d} characters".format(picFilePath, len(file)))

    txtEnc = xorfunc(cipher, file)
    # print("\nencryptedHEX: ", '[{}]'.format(' ' .join(hex(x) for x in txtEnc)))

    byteEnc = fileHeader
    byteEnc += txtEnc[54:]
    open(picEncFilePath, "wb").write(byteEnc)

    txtDec = xorfunc(cipher, txtEnc)

    open(picDec, "wb").write(txtDec)


def generateRndBMPFile(picEncFilePath, cipher=os.urandom(fileLength)):
    byteEnc = fileHeader
    byteEnc += cipher[54:]
    open(picEncFilePath, "wb").write(byteEnc)


if __name__ == '__main__':
    encryptBMPFile(pic1, pic1Enc)
    encryptBMPFile(pic2, pic2Enc)
    generateRndBMPFile(pic3Enc)
