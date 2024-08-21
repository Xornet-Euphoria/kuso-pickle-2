import obfuscator, vm_info

org_key = b"Zhu_Yuan_Qingyi_"
expanded_key = org_key * (256 // len(org_key)) + org_key[0:len(org_key) % 16]

assert len(expanded_key) == 256

crafter = obfuscator.Obfuscator(do_obfuscate=True)


# copyreg._extension_cache[vm_info.key_stream]
# = builtins.list(builtins.range(256))
crafter.get_ctx()
crafter.push_int(vm_info.key_stream)
crafter.obf_import_from("builtins", "list")
crafter.obf_import_from("builtins", "range")
crafter.push_int(256)
crafter.call_f(1)
crafter.call_f(1)
crafter.set_item()

crafter.mark()

# prepare
# key_stream.__getitem__ 
crafter.push_int(vm_info.key_stream_get)
crafter.push_native_function("getattr")
crafter.ext2(vm_info.key_stream)
crafter.push_str("__getitem__")
crafter.call_f(2)

# and key_stream.__setitem__
crafter.push_int(vm_info.key_stream_set)
crafter.push_native_function("getattr")
crafter.ext2(vm_info.key_stream)
crafter.push_str("__setitem__")
crafter.call_f(2)

# reg3 = 0
crafter.push_int(vm_info.reg3)
crafter.push_int(0)

crafter.set_items()

"""
reg3 = 0
for i in range(256):
    # reg3 =
    # int.__div__(
    #   int.__add__(
    #       int.__add__(
    #           reg3, key_stream.__getitem__(i)
    #       ),
    #       expanded_key[i]  # hard-coding
    #   ),
    #   256
    # )
    reg3 = (reg3 + key_stream[i] + expanded_key[i]) % 256

    reg4 = key_stream[i]
    key_stream[i] = key_stream[reg3]
    key_stream[reg3] = reg4
"""
for i in range(256):
    crafter.mark()
    # reg3 = (reg3 + key_stream[i] + expanded_key[i]) % 256
    crafter.push_int(vm_info.reg3)
    crafter.push_native_function("int_mod")
    crafter.push_native_function("int_add")
    crafter.dup()
    crafter.ext1(vm_info.reg3)
    crafter.ext2(vm_info.key_stream_get)
    crafter.push_int(i)
    crafter.call_f(1)
    crafter.call_f(2)
    crafter.push_int(expanded_key[i])  # hard-coding
    crafter.call_f(2)
    crafter.push_int(256)
    crafter.call_f(2)

    # reg4 = key_stream[i]
    crafter.push_int(vm_info.reg4)
    crafter.ext2(vm_info.key_stream_get)
    crafter.push_int(i)
    crafter.call_f(1)

    crafter.set_items()

    # key_stream[i] = key_stream[reg3]
    crafter.ext2(vm_info.key_stream_set)
    crafter.push_int(i)
    crafter.ext2(vm_info.key_stream_get)
    crafter.get_arg3()
    crafter.call_f(1)
    crafter.call_f(2)
    crafter.pop()  # pop None by key_stream.__setitem__

    # key_stream[reg3] = reg4
    crafter.ext2(vm_info.key_stream_set)
    crafter.get_arg3()
    crafter.get_arg4()
    crafter.call_f(2)
    crafter.pop()


# export
ksa_bytecode = crafter.get_payload(check_stop=True)

# test
s = [x for x in range(256)]

j = 0
for i in range(256):
    j = j + s[i] + expanded_key[i]
    j %= 256
    s[i], s[j] = s[j], s[i]

