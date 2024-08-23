import hashlib

l = len(open("./flag.txt", "rb").read())
salt = b"unko-chinko-manko"

org_msg = [str(i * 114514 + 1919810).encode() + salt for i in range(l)]

matrix = [
    hashlib.sha3_512(m).digest()[:l] for m in org_msg
]

gomi = [(i * 931 + 810 % 1337) for i in range(l)]