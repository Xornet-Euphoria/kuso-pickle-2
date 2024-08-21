import obfuscator


crafter = obfuscator.Obfuscator(do_obfuscate=True)

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
crafter.get_arg1()
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
#           hashlib.sha256, 
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
crafter.get_arg2()
crafter.call_f(1)

crafter.memoize()  # 6: index of _extension_cache
crafter.pop()
crafter.get_memo(5)
crafter.push_str("__getitem__")
crafter.call_f(2)
crafter.get_memo(6)
crafter.call_f(1)

crafter.add_op("STACK_GLOBAL")

# export
api_hashing_bytecode = crafter.get_payload(check_stop=True)


# test
if __name__ == "__main__":
    import hashlib, copyreg, vm_info
    module_name = b"builtins"
    elm_name = b"dir"
    module_hash = hashlib.sha3_512(module_name).hexdigest()
    elm_hash = hashlib.sha3_512(elm_name).hexdigest()
    ec = copyreg._extension_cache
    ec[vm_info.ctx] = ec
    ec[vm_info.reg1] = module_hash
    ec[vm_info.reg2] = elm_hash

    import pickle

    # res = crafter.loads()
    res = pickle.loads(crafter.get_payload(check_stop=True))
    print(res)