import pickle
import pickletools
import copyreg
ec = copyreg._extension_cache

ext_dict = {
    16: "ctx",
    129: "unknown",
    130: "input?",
    132: "unknown2",
    134: "unknown3",
    131: "unknown4",
    13056: "result"
}

def mydis(pickle_bytes):
    g = pickletools.genops(pickle_bytes)

    for opcode, arg, pos in g:
        name = opcode.name
        if name == "BINBYTES":
            arg = "(snipped)"
        elif name in ["EXT1", "EXT2", "EXT4"]:
            info = ext_dict[arg] if arg in ext_dict else None
            arg = f"{arg} ({info})"  if info is not None else f"{arg} ({ec[arg]})" 

        print(f"[{pos}] {name}: {arg}")


with open("./chall.pkl", "rb") as f:
    pkl = f.read()

first_step = pkl[:10482]
init = pickle.loads(first_step + pickle.STOP)

set_copyreg = pickle.loads(init)

# mydis(pkl)

input_bytecode = ec[130]
# mydis(input_bytecode)

_input = pickle.loads(input_bytecode)

flag_length = 56

import z3
# input_bv = z3.BitVec("input", flag_length)
input_bv = [z3.Int(f"input_{i}") for i in range(flag_length)]

# patch
input_idx = 12288
add_idx = 193
mul_idx = 194
eq_idx = 198

ec[input_idx] = input_bv
ec[add_idx] = lambda x, y: x + y
ec[mul_idx] = lambda x, y: x * y
ec[eq_idx] = lambda x, y: print(f"{x}, ", end="") or True  # if result is false, next operation will fail.

third = pickle.loads(ec[132])

res_idx = 13056

forth = pickle.loads(ec[134])

# mydis(ec[134])

target = [777608, 732754, 589323, 634380, 705876, 732504, 700040, 653799, 701951, 606866, 650760, 707791, 635433, 774691, 725287, 662287, 621134, 688301, 698696, 594769, 816833, 627640, 680818, 669979, 668393, 770865, 617394, 558903, 725342, 694882, 716532, 654891, 712000, 635559, 715192, 580986, 782500, 762735, 668963, 670527, 711679, 680067, 708304, 722481, 647503, 707975, 694053, 658708, 590330, 741846, 615948, 684794, 815580, 626108, 803846, 650642]

solver = z3.Solver()
for x, y in zip(target, ec[res_idx]):
    solver.add(x == y)

res = solver.check()

assert res == z3.sat
flag = ""

m = solver.model()
for bv in input_bv:
    flag += chr(m[bv].as_long())

print(flag)