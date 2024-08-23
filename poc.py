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
crafter.pop()

# second stage: matrix multiplication with recursion
crafter.call_pickle_bytecode("matrix_mul")
crafter.pop()

# third stage: check
crafter.call_pickle_bytecode("check_input")
crafter.pop()

# epilogue: clear copyreg._extension_cache
crafter.call_pickle_bytecode("epilogue")
# crafter.pop()

# crafter.dis()

payload = crafter.get_payload(check_stop=True)
with open("chall.pkl", "wb") as f:
    f.write(payload)
import pickle
res = pickle.loads(payload)
print(res)


# test
import copyreg
print("=" * 0x40)
print(copyreg._extension_cache)
