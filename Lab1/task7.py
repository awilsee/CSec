import hashlib
import os


def one_wayness():
    #txt = input("Enter string to hash: ")
    #print(hashlib.sha256(txt.encode()).hexdigest())

    print("10 example hashes:")
    for i in range(10):
        print(hashlib.sha256(os.urandom(256)).hexdigest())


    print("\n2 hashes with hamming distance:")
    print(hashlib.sha256("Example string 1".encode()).hexdigest())
    print(hashlib.sha256("Example string 2".encode()).hexdigest())
    print()


def preimage_res(target):
    print("Call for target: 0x{:064X}" .format(target))

    hash_val = 0
    i = 1
    while True:
        hash_val = int.from_bytes(hashlib.sha256(os.urandom(256)).digest(), 'big')
        if target > hash_val:
            break
        i += 1
        #if 0 == i % 1000:
        #    print("#Inputs: {} still calculating...".format(i))
    print("#Inputs: {}\n targetVal: 0x{:064X}\n digest: \t0x{:064X}\n" .format(i, target, hash_val))
    return i


if __name__ == '__main__':
    one_wayness()

    t1 = 0x0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    t2 = 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    t3 = 0x000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    t4 = 0x0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    t5 = 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    preimage_res(t1)
    preimage_res(t2)
    preimage_res(t3)
    preimage_res(t4)
    preimage_res(t5)

