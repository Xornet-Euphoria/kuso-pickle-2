import obfuscator
import vm_info

l = len(open("./flag.txt", "rb").read())

# shorten
int_add = vm_info.native_function_idx["int_add"]
int_mul = vm_info.native_function_idx["int_mul"]

crafter = obfuscator.Obfuscator(do_obfuscate=True)

# main
# sum(map(builtins.int.__mul__, b_input, bs[reg1]))

# stash reg1 to memo
crafter.get_arg1()
crafter.put_memo(1)
crafter.pop()

crafter.ext2(vm_info.mul_res)
crafter.obf_import_from("builtins", "sum")
crafter.obf_import_from("builtins", "map")
crafter.push_native_function("int_mul")
crafter.ext2(vm_info.inp)
crafter.ext2(vm_info.matrix_get)
crafter.get_memo(1)

crafter.call_f(1)  # matrix getter

crafter.call_f(3)  # map
crafter.call_f(1)  # sum
crafter.add_op("APPEND")


# set loop-count (increment)
crafter.get_ctx()
crafter.push_int(1)
crafter.ext1(int_add)
crafter.get_memo(1)
crafter.push_int(1)
crafter.call_f(2)
crafter.set_item()
crafter.pop()

# check loop-count
# table[builtins.int.__floordiv__(reg1, 3)](bc)
# -> table[0](bc) or table[1](bc)
# -> pickle.loads(bc) or builtins.id(bc)
crafter.push_native_function("getattr")
crafter.ext4(vm_info.rec_table)
crafter.push_str("__getitem__")
crafter.call_f(2)

crafter.push_native_function("int_div")
crafter.get_arg1()
crafter.push_int(l)
crafter.call_f(2)

# call next function (pickle.loads or builtins.id)
crafter.call_f(1)
crafter.ext4(vm_info.function_idx["rec_mul"])
crafter.call_f(1)

# export
recursive_mul_bytecode = crafter.get_payload(check_stop=True)
