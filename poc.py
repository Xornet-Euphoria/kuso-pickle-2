import obfuscator, vm_info
import second_poc


crafter = obfuscator.Obfuscator()

crafter.import_from("pickle", "loads")
crafter.push_bytes(second_poc.create_vm_ctx)
crafter.call_f(1)
crafter.pop()

crafter.start_obfuscation()

# todo: junk code stage
# - push and pop
# - set same index in memo

# first stage: length check

crafter.call_pickle_bytecode("get_input")
# crafter.pop()

# second stage: custom RC4?
# https://en.wikipedia.org/wiki/RC4

# 2-1: KSA
crafter.call_pickle_bytecode("ksa")

# 2-2: PRGA

# third stage: check

# epilogue: clear copyreg._extension_cache
# crafter.call_pickle_bytecode("epilogue")
# crafter.pop()

# crafter.dis()

import pickle
# res = crafter.loads()
res = pickle.loads(crafter.get_payload(check_stop=True))
print(res)


import copyreg
print("=" * 0x40)
print(copyreg._extension_cache)

import ksa
print(ksa.s == copyreg._extension_cache[vm_info.key_stream])