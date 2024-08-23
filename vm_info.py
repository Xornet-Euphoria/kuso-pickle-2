import hashlib

def h(b: bytes | str):
    if isinstance(b, str):
        b = b.encode()

    return hashlib.sha3_512(b).hexdigest()

# VM specification area (idx)

# pseudo registers
ctx = 0x10  # 0 is forbidden
reg1 = 1
reg2 = 2
reg3 = 3
reg4 = 4
reg5 = 5
reg6 = 6
reg7 = 7
reg8 = 8


function_idx = {
    "api_hashing": 0x81,
    "get_input": 0x82,
    "epilogue": 0x83,
    "matrix_mul": 0x84,
    "rec_mul": 0x85,
    "check_input": 0x86
}

assert min(function_idx.values()) > 0x80
assert max(function_idx.values()) < 0xc0

native_function_idx = {
    "int_add": 0xc1,
    "int_mul": 0xc2,
    "call_bytecode": 0xc3,
    "getattr": 0xc4,
    "int_div": 0xc5,
    "int_eq": 0xc6
}

assert min(native_function_idx.values()) > 0xc0
assert max(native_function_idx.values()) < 0x100

# memory address (index) used functions
key = 0x1000
key_stream = 0x2000
key_stream_get = 0x2100
key_stream_set = 0x2200
inp = 0x3000
rec_table = 0x3100
matrix_get = 0x3200
mul_res = 0x3300

# constants

constant_strings_list = [
    "pickle", "loads", "__getitem__", "__setitem__", "encode", "builtins", "getattr", "list", "map", "_hashlib", "HASH", "hexdigest", "sha3_512", "hashlib", "str", "sys", "modules", "keys", "index", "dir", "__floordiv__", "int"
]

# check unique
assert len(constant_strings_list) == len(set(constant_strings_list))


hashed_strings = [
    "builtins", "getattr", "exit", "dir", "len", "input", "copyreg", "clear_extension_cache", "list", "range", "sum", "map", "id", "print", "all"
]

constant_number_start = 0x10000
string_start = 0x20000
hash_start = 0x30000

constant_strings = {
    s: string_start + idx for idx, s in enumerate(constant_strings_list)
}

hashes = {
    h(s): hash_start + idx for idx, s in enumerate(hashed_strings)
}