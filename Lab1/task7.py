import hashlib
import math
import os
import time
import matplotlib.pyplot as plt

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

    i = 1
    while True:
        hash_val = int.from_bytes(hashlib.sha256(os.urandom(20)).digest(), 'big')
        if target > hash_val:
            break
        i += 1
    print("#Inputs: {}\n targetVal: 0x{:064X}\n digest: \t0x{:064X}\n" .format(i, target, hash_val))
    return i


def collision_res():
    num_of_loops = 3

    bits_list = [list() for x in range(num_of_loops)]
    dict_list = [list() for x in range(num_of_loops)]
    time_list = [list() for x in range(num_of_loops)]

    dict_hashs = dict()

    for i in range(num_of_loops):
        print("test {}".format(i))
        bits = 8
        while 50 >= bits:
            bits_list[i].append(bits)
            start_time = time.process_time()
            while True:
                value = os.urandom(20)
                # generate key and get only desired number of bytes
                key = int.from_bytes(hashlib.sha256(os.urandom(20)).digest()[0:(math.ceil(bits / 8))], 'big')
                # shift bytes so only 12 bits are left for comparison
                key = key >> ((math.ceil(bits / 8) * 8) - bits)
                # create dict
                if key in dict_hashs:
                    if value != dict_hashs[key]:
                        elapsed_time = (time.process_time() - start_time)
                        time_list[i].append(elapsed_time)
                        dict_list[i].append(len(dict_hashs) / 1000)
                        print("Found duplicate with {} bits, needed {:.0f} s #inputs {}k\nhash1: 0x{:020X}\nInput1: 0x{:040X}\nInput2: 0x{:040X}\n" .format(bits, elapsed_time, len(dict_hashs), key, int.from_bytes(dict_hashs[key], 'big'), int.from_bytes(value, 'big')))
                        break
                else:
                    dict_hashs[key] = value
            dict_hashs.clear()
            bits += 2

    #calculate mean
    bits_mean_list = []
    dict_mean_list = []
    time_mean_list = []
    for i in range(len(bits_list[0])):
        bits_mean = 0
        dict_mean = 0
        time_mean = 0
        for j in range(num_of_loops):
            bits_mean += bits_list[j][i]
            dict_mean += dict_list[j][i]
            time_mean += time_list[j][i]
        bits_mean_list.append(bits_mean/float(num_of_loops))
        dict_mean_list.append(dict_mean/float(num_of_loops))
        time_mean_list.append(time_mean/float(num_of_loops))

    print(bits_mean_list)
    print(dict_mean_list)
    print(time_mean_list)

    #plotting graphs
    fig = plt.figure()
    plt.plot(bits_mean_list, dict_mean_list)
    plt.xlabel('digest size [bits]')
    plt.ylabel('# of inputs [k]')
    fig.savefig('plot_num_input.png', dpi=500, bbox_inches='tight')

    fig = plt.figure()
    plt.plot(bits_mean_list, time_mean_list)
    plt.xlabel('digest size [bits]')
    plt.ylabel('collision time [s]')
    fig.savefig('plot_time.png', dpi=500, bbox_inches='tight')


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

    collision_res()
