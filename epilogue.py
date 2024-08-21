import obfuscator


# copyreg.clear_extension_cache()
crafter = obfuscator.Obfuscator(do_obfuscate=True)

crafter.obf_import_from("copyreg", "clear_extension_cache")
crafter.call_f(0)

# export
epilogue_bytecode = crafter.get_payload(check_stop=True)