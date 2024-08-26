import pickle
import pickletools

with open("./chall.pkl", "rb") as f:
    pkl = f.read()

first_step = pkl[:10482]
init = pickle.loads(first_step + pickle.STOP)

set_copyreg = pickle.loads(init)

import copyreg
ec = copyreg._extension_cache

matrix_mul = ec[132]
matrix = pickle.loads(matrix_mul[:3464] + pickle.STOP)

second_step = pkl[:10503]
check = pickle.loads(second_step + pickle.STOP)

res = pickle.loads(check[:788] + pickle.STOP)

print(res)