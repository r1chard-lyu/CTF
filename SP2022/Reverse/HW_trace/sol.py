with open("cs_2022","rb") as fp:
    str1=fp.read()

    #"\xe8\xef\xbe\xad\xde\xcc\xcb\xe8" -> "\x90\x90\x90\x90\x90\x90\x90\x90"
    str2=str1.replace(b"\xe8\xef\xbe\xad\xde\xcc\xcb\xe8", b"\x90\x90\x90\x90\x90\x90\x90\x90")

    print(str1.count(b"\xe8\xef\xbe\xad\xde\xcc\xcb\xe8"))
    print(str1.count(b"\x90\x90\x90\x90\x90\x90\x90\x90"))


with open("finish_file", "wb") as binary_file:
    binary_file.write(str2)
    print(str2.count(b"\xe8\xef\xbe\xad\xde\xcc\xcb\xe8"))
    print(str2.count(b"\x90\x90\x90\x90\x90\x90\x90\x90"))


