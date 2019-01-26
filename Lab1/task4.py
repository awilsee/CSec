import os

import task3


def xorImages(pic1FilePath, pic2FilePath):
    file1 = open(pic1FilePath, "rb").read()
    file2 = open(pic2FilePath, "rb").read()
    print("file {} has {:d} characters".format(pic1FilePath, len(file1)))

    txtEnc = task3.xorfunc(file1, file2)
    # print("\nencryptedHEX: ", '[{}]'.format(' ' .join(hex(x) for x in txtEnc)))

    task3.write_bmp_file("./xorPics.bmp", txtEnc)


if __name__ == '__main__':
    cipher = os.urandom(task3.fileLength)
    task3.encryptBMPFile(task3.pic1, task3.pic1Enc, cipher)
    task3.encryptBMPFile(task3.pic2, task3.pic2Enc, cipher)
    task3.generateRndBMPFile(task3.pic3Enc, cipher)
    xorImages(task3.pic1Enc, task3.pic2Enc)
