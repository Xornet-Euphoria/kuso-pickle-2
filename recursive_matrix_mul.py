import obfuscator, vm_info


crafter = obfuscator.Obfuscator(do_obfuscate=True)

# setup
crafter.get_ctx()
crafter.mark()

# 1-1: function table
crafter.push_int(vm_info.rec_table)
crafter.mark()
crafter.push_native_function("call_bytecode")
crafter.obf_import_from("builtins", "id")
crafter.add_op("LIST")

# 1-2: matrix (getter)
crafter.push_int(vm_info.matrix_get)
crafter.push_native_function("getattr")
crafter.mark()

import chall_ins
for b in chall_ins.matrix:
    crafter.push_bytes(b)

crafter.add_op("LIST")
crafter.push_str("__getitem__")
crafter.call_f(2)

# 1-3: result
crafter.push_int(vm_info.mul_res)
crafter.add_op("EMPTY_LIST")

# 1-4: reg1
crafter.set_arg1()
crafter.push_int(0)

crafter.set_items()
crafter.pop()

# recurrrrrrrrrrrr
crafter.call_pickle_bytecode("rec_mul")

# export
matrix_mul_bytecode = crafter.get_payload(check_stop=True)