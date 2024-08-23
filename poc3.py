import obfuscator
import copyreg
import vm_info

# test index (not used in challenge)
int_add = vm_info.native_function_idx["int_add"]
int_mul = 0xc6
bc_idx = 0x40000
table = 0x50000
matrix_get = 0x60000

crafter = obfuscator.Obfuscator()

# main
# test: print(i)
# challenge: sum(map(builtins.int.__mul__, b_input, bs[reg1]))
crafter.import_from("builtins", "print")  # debug
crafter.import_from("builtins", "sum")
crafter.import_from("builtins", "map")
crafter.ext1(int_mul)
crafter.ext4(vm_info.inp)
crafter.ext4(matrix_get)
crafter.get_arg1()
crafter.call_f(1)  # matrix getter
crafter.call_f(3)  # map
crafter.call_f(1)  # sum

crafter.call_f(1)  # print
crafter.pop()

# set loop-count (increment)
crafter.get_ctx()
crafter.push_int(1)
crafter.ext1(int_add)
crafter.get_arg1()
crafter.push_int(1)
crafter.call_f(2)
crafter.set_item()
crafter.pop()

# check loop-count
# table[builtins.int.__floordiv__(reg1, 3)](bc)
# -> table[0](bc) or table[1](bc)
# -> pickle.loads(bc) or builtins.id(bc)
crafter.import_from("builtins", "getattr")
crafter.ext4(table)
crafter.push_str("__getitem__")
crafter.call_f(2)

crafter.import_from("builtins", "getattr")
crafter.import_from("builtins", "int")
crafter.push_str("__floordiv__")
crafter.call_f(2)
crafter.get_arg1()
crafter.push_int(3)
crafter.call_f(2)

# call next function (pickle.loads or builtins.id)
crafter.call_f(1)
crafter.ext4(bc_idx)
crafter.call_f(1)

# export
recursive_loads = crafter.get_payload(check_stop=True)


if __name__ == "__main__":
    ec = copyreg._extension_cache
    ec[vm_info.ctx] = ec
    ec[1] = 0

    ec[int_add] = int.__add__
    ec[int_mul] = int.__mul__
    ec[bc_idx] = recursive_loads
    import pickle
    ec[table] = [pickle.loads, id]

    raw_matrix = [
        b"asdf" * 14,
        b"qwer" * 14,
        b"zxcv" * 14
    ]

    ec[matrix_get] = raw_matrix.__getitem__

    flag = open("./true_flag.txt", "rb").read()
    ec[vm_info.inp] = flag

    # random 56x56bytes

    res = crafter.loads()

    print(ec)
    print(res)