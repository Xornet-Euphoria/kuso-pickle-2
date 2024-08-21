import obfuscator


# return: arg1 % arg2
# arg1.__mod__(arg2)
# builtins.getattr(arg1, "__mod__")(arg2)
crafter = obfuscator.Obfuscator(do_obfuscate=True)