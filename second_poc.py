# todo: ハッシュ値の難読化

import hashlib
import obfuscator, vm_info

# list(
#   map(
#       _hashlib.HASH.hexdigest, 
#       map(
#           hashlib.sha256, 
#           map(
#               builtins.str.encode, 
#               sys.modules.keys()
#           )
#       )
#   )
# )

flag = open("./flag.txt", "rb").read()
l = len(flag)
assert l <= 256

copyreg_hash = hashlib.sha3_512(b"copyreg").hexdigest()
extension_cache_hash = hashlib.sha3_512(b"_extension_cache").hexdigest()

crafter = obfuscator.Obfuscator()

crafter.import_from("builtins", "getattr")
crafter.memoize()  # 0
crafter.import_from("builtins", "list")
crafter.get_memo(0)

crafter.import_from("builtins", "list")
crafter.import_from("builtins", "map")
crafter.get_memo(0)
crafter.import_from("_hashlib", "HASH")
crafter.push_str("hexdigest")
crafter.call_f(2)

crafter.import_from("builtins", "map")
crafter.import_from("hashlib", "sha3_512")

crafter.import_from("builtins", "map")
crafter.get_memo(0)
crafter.import_from("builtins", "str")
crafter.push_str("encode")
crafter.call_f(2)
crafter.get_memo(0)
crafter.import_from("sys", "modules")
crafter.memoize()  # 1: dict of modules
crafter.push_str("keys")
crafter.call_f(2)
crafter.call_f()
crafter.memoize()  # 2: dict_keys of module

crafter.call_f(2)
crafter.call_f(2)
crafter.call_f(2)
crafter.call_f(1)

crafter.push_str("index")
crafter.call_f(2)
crafter.push_str(copyreg_hash)
crafter.call_f(1)

crafter.memoize()  # 3: index of copyreg
crafter.pop()
crafter.get_memo(2)
crafter.call_f(1)
crafter.push_str("__getitem__")
crafter.call_f(2)
crafter.get_memo(3)
crafter.call_f(1)
crafter.memoize()  # 4: module name ("copyreg")

# list(
#   map(
#       _hashlib.HASH.hexdigest, 
#       map(
#           hashlib.sha3_512, 
#           map(
#               builtins.str.encode, 
#               dir(sys.modules["copyreg"])
#           )
#       )
#   )
# )

crafter.get_memo(0)
crafter.get_memo(0)

crafter.import_from("builtins", "list")
crafter.import_from("builtins", "map")
crafter.get_memo(0)
crafter.import_from("_hashlib", "HASH")
crafter.push_str("hexdigest")
crafter.call_f(2)

crafter.import_from("builtins", "map")
crafter.import_from("hashlib", "sha3_512")

crafter.import_from("builtins", "map")
crafter.get_memo(0)
crafter.import_from("builtins", "str")
crafter.push_str("encode")
crafter.call_f(2)

crafter.import_from("builtins", "dir")
crafter.get_memo(0)
crafter.get_memo(1)
crafter.push_str("__getitem__")
crafter.call_f(2)
crafter.get_memo(4)
crafter.call_f(1)
crafter.call_f(1)
crafter.memoize()  # 5: dir(copyreg)

crafter.call_f(2)
crafter.call_f(2)
crafter.call_f(2)
crafter.call_f(1)

crafter.push_str("index")
crafter.call_f(2)
crafter.push_str(extension_cache_hash)
crafter.call_f(1)

crafter.memoize()  # 6: index of _extension_cache
crafter.pop()
crafter.get_memo(5)
crafter.push_str("__getitem__")
crafter.call_f(2)
crafter.get_memo(6)
crafter.call_f(1)

crafter.add_op("STACK_GLOBAL")
crafter.memoize()  # 7: _extension_cache

# init vm context

import api_hashing, get_input, epilogue, ksa

# function table
bytecodes = {
    "api_hashing": api_hashing.api_hashing_bytecode,
    "get_input": get_input.get_input_bytecode,
    "epilogue": epilogue.epilogue_bytecode,
    "ksa": ksa.ksa_bytecode
}

assert set(bytecodes.keys()) == set(vm_info.function_idx.keys())

function_table = {
    k: (vm_info.function_idx[k], v) for k, v in bytecodes.items()
}

# constants
nums = [x for x in range(256)]

crafter.mark()
crafter.push_int(vm_info.ctx)
crafter.get_memo(7)

# set function (pickle bytecode)
for _, (idx, bc) in function_table.items():
    crafter.set_byte(idx, bc)

# set native function (not pickle bytecode)
import subroutines
native_function_table = {
    k: (vm_info.native_function_idx[k], v) for k, v in subroutines.native_function_bytecode.items()
}

for _, (idx, bc) in native_function_table.items():
    crafter.push_int(idx)
    crafter.add_payload(bc)

# set constants
for n in nums:
    idx = n + vm_info.constant_number_start
    crafter.push_int(idx)
    crafter.push_int(n)

for s, idx in vm_info.constant_strings.items():
    crafter.push_int(idx)
    crafter.push_str(s)

for h, idx in vm_info.hashes.items():
    crafter.push_int(idx)
    crafter.push_str(h)

# set pre-defined variables

crafter.add_op("SETITEMS")

create_vm_ctx = crafter.get_payload(check_stop=True)

if __name__ == "__main__":
    crafter.dis()

    res = crafter.loads()

    assert res == res[vm_info.ctx]