import obfuscator

flag = open("./flag.txt").read()
l = len(flag)
assert l <= 256


crafter = obfuscator.Obfuscator(do_obfuscate=True)

# todo: junk code stage
# - push and pop
# - set same index in memo

# first stage: length check
crafter.obf_import_from("builtins", "getattr")
crafter.memoize()  # 0
crafter.mark()
crafter.obf_import_from("builtins", "exit")
for _ in range(l-1):
    crafter.dup()
crafter.obf_import_from("builtins", "dir")  # no arg function
crafter.obf_import_from("builtins", "exit")
for _ in range(256-l-1):
    crafter.dup()
crafter.add_op("LIST")
crafter.push_str("__getitem__")
crafter.call_f(2)

crafter.obf_import_from("builtins", "len")
crafter.get_memo(0)
# todo: prompt?
crafter.obf_import_from("builtins", "input")
crafter.call_f(0)
crafter.push_str("encode")
crafter.call_f(2)
crafter.call_f(0)
crafter.memoize()  # 1

crafter.call_f(1)
crafter.call_f(1)
crafter.call_f(0)

crafter.pop()  # pop the result of dir()

# set input().encode() to copyreg._extension_cache[idx]
crafter.get_memo(1)  # user_input.encode()

# export
get_input_bytecode = crafter.get_payload(check_stop=True)