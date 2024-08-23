import obfuscator, chall_ins, vm_info

crafter = obfuscator.Obfuscator(do_obfuscate=True)

target = [777608, 732754, 589323, 634380, 705876, 732504, 700040, 653799, 701951, 606866, 650760, 707791, 635433, 774691, 725287, 662287, 621134, 688301, 698696, 594769, 816833, 627640, 680818, 669979, 668393, 770865, 617394, 558903, 725342, 694882, 716532, 654891, 712000, 635559, 715192, 580986, 782500, 762735, 668963, 670527, 711679, 680067, 708304, 722481, 647503, 707975, 694053, 658708, 590330, 741846, 615948, 684794, 815580, 626108, 803846, 650642]

crafter.obf_import_from("builtins", "print")
crafter.push_native_function("getattr")
crafter.mark()
crafter.push_str("no")
crafter.push_str("ok")
crafter.add_op("LIST")
crafter.push_str("__getitem__")
crafter.call_f(2)

crafter.obf_import_from("builtins", "all")
crafter.obf_import_from("builtins", "map")
crafter.push_native_function("int_eq")
crafter.mark()
for x, y in zip(target, chall_ins.gomi):
    z = x - y
    crafter.push_native_function("int_add")
    crafter.push_int(z)
    crafter.push_int(y)
    crafter.call_f(2)

crafter.add_op("LIST")
crafter.ext2(vm_info.mul_res)
crafter.call_f(3)
crafter.call_f(1)

crafter.call_f(1)  # getitem for ["no", "ok"]
crafter.call_f(1)  # print

# export
check_input_bytecode = crafter.get_payload(check_stop=True)