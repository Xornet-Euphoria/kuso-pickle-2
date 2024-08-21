import pickaxe

native_function_bytecode = {}

# int.__add__(x, y)
crafter = pickaxe.Crafter()
crafter.import_from("builtins", "getattr")
crafter.import_from("builtins", "int")
crafter.push_str("__add__")
crafter.call_f(2)

# export
native_function_bytecode["int_add"] = crafter.get_payload()
crafter.clear()

# int.__mod__(x, y)
crafter.import_from("builtins", "getattr")
crafter.import_from("builtins", "int")
crafter.push_str("__mod__")
crafter.call_f(2)

# export
native_function_bytecode["int_mod"] = crafter.get_payload()
crafter.clear()

# pickle.loads(x)
crafter.import_from("pickle", "loads")

# export
native_function_bytecode["call_bytecode"] = crafter.get_payload()
crafter.clear()

# bytes.__getitem__(x, y)
crafter.import_from("builtins", "getattr")
crafter.import_from("builtins", "bytes")
crafter.push_str("__getitem__")
crafter.call_f(2)

# export
native_function_bytecode["bytes_at"] = crafter.get_payload()
crafter.clear()

# builtins.getattr(x, y)
crafter.import_from("builtins", "getattr")

native_function_bytecode["getattr"] = crafter.get_payload()
crafter.clear()