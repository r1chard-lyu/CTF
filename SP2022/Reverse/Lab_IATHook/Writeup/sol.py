arr = bytearray.fromhex('7DD24076A714B4DC')
enc_flag = bytearray.fromhex('113E2E291C1E333B312F383D04422A32011C0F0032300016262A')
ModuleName = bytearray.fromhex('16B73218C27887EE53B62C1AA753D1A82DA02F15E670D0AE18A13376E071C09112B6351AC25CD5B219BE2537A742DDAE09A7211AF766DBA818B13476D267D1AE4EE06E12CB78B49118A13317C071F6B305934035C866C6B91EA640')
wrong = [87, 114, 111, 110, 103]
def dec(ModuleName, arr, count, offset):
    for i in range(count):
        ModuleName[i] ^= arr[i % offset]
    return ModuleName
FLAG = dec(enc_flag, wrong, 26, len(wrong))
print(FLAG)