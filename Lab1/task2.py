import binascii
import os

from task1 import xorfunc

filePath = "./txtFile"
filePathEnc = "./txtFileEnc"

file = open(filePath, "rb").read()
print("file {} has {:d} characters" .format(filePath, len(file)))
print("filetxt: ", file)

cipher = os.urandom(len(file))
#print("cipherKeyHEX: ", binascii.hexlify(cipher))

txtEnc = xorfunc(cipher, file)
print("\nencryptedHEX: ", '[{}]'.format(' ' .join(hex(x) for x in txtEnc)))

fileEnc = open(filePathEnc, "wb").write(txtEnc)

txtDec = xorfunc(cipher, txtEnc)

print("\ndecrypted: ", txtDec.decode("utf-8"))