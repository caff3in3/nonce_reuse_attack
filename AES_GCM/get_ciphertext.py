from pwn import xor

pt = b'AESGCM keeps data safe and sound'
ct = 'a3a82054ac7ebc2054ad5280076d512f7490bb936a1556b838c6f2115f7bb240'
pt_target = 'fe019ac0355a841fd3e60e6c037194513348d9f4c7ab186c56e78cbed2587b25'

key_stream = xor(bytes.fromhex(ct), pt)
ct_target = xor(key_stream, bytes.fromhex(pt_target))
print(ct_target.hex())