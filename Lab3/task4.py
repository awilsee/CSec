import base64
import hashlib

pw_file = "./passwordfile.txt"
dict_file = "/usr/share/dict/words"
dict_file2 = "./passwords-dict.txt"


def read_userpw_file():
    entries = []
    with open(pw_file, 'r') as f:
        for line_terminated in f:
            username, pwhash = line_terminated.split(':')
            entry = [username, pwhash.rstrip().split('}')[1]]
            entries.append(entry)
    return entries


def calc_hash_try_crack(file_path, userpw_entries):
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        for line_terminated in f:
            line = line_terminated.rstrip('\n')
            b64_hash = base64.b64encode(hashlib.sha1(line.encode('utf-8')).digest())
            for userpw in userpw_entries:
                if b64_hash.decode() == userpw[1]:
                    print("User {} has used PW: {}".format(userpw[0], line))
                    break


if __name__ == '__main__':
    userpw_entries = read_userpw_file()
    calc_hash_try_crack(dict_file, userpw_entries)
    calc_hash_try_crack(dict_file2, userpw_entries)
