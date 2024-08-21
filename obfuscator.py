import pickaxe, hashlib, vm_info


# todo
# - complicated calling convention
#   - multi index
class Obfuscator(pickaxe.Crafter):
    def __init__(self, *, forbidden_bytes: list[bytes] | list[int] = [], check_stop=False, do_obfuscate=False) -> None:
        super().__init__(forbidden_bytes=forbidden_bytes, check_stop=check_stop)

        self.obfuscation = do_obfuscate


    def start_obfuscation(self):
        self.obfuscation = True


    def ext1(self, idx: int):
        assert idx < 0x100
        self.add_op("EXT1")
        self._add_number1(idx)


    def ext2(self, idx: int):
        assert idx < 0x10000
        self.add_op("EXT2")
        self._add_number2(idx)


    def ext4(self, idx: int):
        assert idx < 0x100000000
        self.add_op("EXT4")
        self._add_number4(idx)


    def get_ctx(self):
        self.ext1(vm_info.ctx)


    def get_arg(self, n: int):
        if n <= 0 and n > 8:
            raise ValueError("the number of register is 8")
        
        self.ext1(n)


    def get_arg1(self):
        self.get_arg(vm_info.reg1)


    def get_arg2(self):
        self.get_arg(vm_info.reg2)


    def get_arg3(self):
        self.get_arg(vm_info.reg3)


    def get_arg4(self):
        self.get_arg(vm_info.reg4)


    def push_bytes(self, b: bytes):
        self.add_op("BINBYTES")
        self._add_number4(len(b))
        self.add_payload(b)


    def set_byte(self, idx: int, b: bytes):
        self.push_int(idx)
        self.push_bytes(b)


    def set_item(self):
        self.add_op("SETITEM")


    def set_items(self):
        self.add_op("SETITEMS")


    def set_arg1(self):
        self.push_int(1)


    def set_arg2(self):
        self.push_int(2)


    def obf_import_from(self, module: str | bytes, name: str | bytes):
        assert self.obfuscation, "obfuscation is disabled"
        h_module = vm_info.h(module)
        h_name = vm_info.h(name)

        # assumption:
        # copyreg._extension_cache[0] = copyreg._extension_cache
        #                         [?] = api_hashing.api_hashing_bytecode
        self.get_ctx()
        self.mark()
        self.set_arg1()
        if h_module in vm_info.hashes:
            self.ext4(vm_info.hashes[h_module])
        else:
            self.push_str(h_module)
        self.set_arg2()
        if h_name in vm_info.hashes:
            self.ext4(vm_info.hashes[h_name])
        else:
            self.push_str(h_name)
        self.set_items()
        self.pop()
        self.ext1(vm_info.native_function_idx["call_bytecode"])
        self.ext1(vm_info.function_idx["api_hashing"])
        self.call_f(1)


    def push_int(self, n: int):
        if not self.obfuscation:
            return super().push_int(n)
        
        if n < 0 or n > 0xff:
            return super().push_int(n)
        
        idx = vm_info.constant_number_start + n
        self.ext4(idx)


    def push_str(self, s: str):
        if not self.obfuscation:
            return super().push_str(s)

        if s in vm_info.constant_strings:
            # todo: O(n) -> O(1)
            idx = vm_info.constant_strings[s]
            self.ext4(idx)
        else:
            print("[!] not obfuscated string", s)
            super().push_str(s)


    def push_native_function(self, function_name: str):
        if not self.obfuscation:
            raise ValueError("obfuscation is disabled")
        
        if function_name not in vm_info.native_function_idx:
            raise ValueError(f"{function_name} is not registerd")
        
        self.ext1(vm_info.native_function_idx[function_name])


    def call_pickle_bytecode(self, function_name: str):
        if not self.obfuscation:
            raise ValueError("obfuscation is disabled")
        
        if function_name not in vm_info.function_idx:
            raise ValueError(f"{function_name} is not registerd")

        self.push_native_function("call_bytecode")
        self.ext1(vm_info.function_idx[function_name])
        self.call_f(1)


    def debug_print(self, msg: str = "[DEBUG] Reached here"):
        self.import_from("builtins", "print")
        self.push_str(msg)
        self.call_f(1)
        self.pop()  # eliminate None
