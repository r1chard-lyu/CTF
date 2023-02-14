from Crypto.Cipher import AES
import json



key = b"\x31\x38\x4d\x62\x48\x39\x6f\x45\x6e\x62\x58\x48\x79\x48\x54\x52"
#key = 0x31384d6248396f456e62584879485452
print("FLAG{" + key.decode('utf8') + "}")

with open("stm32f0_aes.json", "r") as f:
    data = json.load(f)

for d in data:
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(bytes(d["ct"]))
    if pt != bytes(d["pt"]):
        print("Wrong!")
        exit(0)

print("Correct!")