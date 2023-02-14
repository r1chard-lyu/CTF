from pwn import *
from binascii import *
from ast import literal_eval

r = remote("edu-ctf.zoolab.org","10006")

st1 = r.recvuntil("?")
str2 = st1.split(b"\n")

#----------- ** tcache chall ** -----------
def byte_to_hex(number):
    return int(number.decode("ascii"),16)

dic = { "A" : byte_to_hex(str2[1][26:30]), "B" : byte_to_hex(str2[2][26:30]), "C" : byte_to_hex(str2[3][26:30]), "D" : byte_to_hex(str2[4][26:30]), "E" : byte_to_hex(str2[5][26:30]), "F" : byte_to_hex(str2[6][26:30]), "G" : byte_to_hex(str2[7][26:30])}
dic_chunk_size ={}
list_0x20 = []
list_0x30 = []
list_0x40 = []
def classfication(char,value):
    print(char,hex(value))
    value += 0x8
    if value <= 0x20 : 
        list_0x20.append(char)
        dic_chunk_size[char] = hex(0x20)
    elif value > 0x20 and value <= 0x30 :
        list_0x30.append(char)
        dic_chunk_size[char] = hex(0x30)
    elif value >= 0x30 and value :
        list_0x40.append(char)
        dic_chunk_size[char] = hex(0x40)


[classfication(str(chr(str2[i][5])) ,dic[ str(chr(str2[i][5])) ]  )for i in range(14,7,-1) ]
print(list_0x20)
print(list_0x30)
print(list_0x40)
chunk_size_0x30 = "".join([str(list_0x30[i])+" --> "  for i in range(len(list_0x30))])+"NULL"
chunk_size_0x40 = "".join([str(list_0x40[i])+" --> "  for i in range(len(list_0x40))])+"NULL"

r.sendline(chunk_size_0x30.encode())
r.sendline(chunk_size_0x40.encode())

#----------- ** address chall ** -----------

st3 = r.recvuntil(";")
st4 = r.recvuntil("?")
address = byte_to_hex(st3[-17:-3])


start = st3[-22]
end = st4[1]

for i in range(end - start):
    address += literal_eval(dic_chunk_size[chr(start)])

r.sendline(hex(address).encode())


#---------- ** index chall ** -----------






r.interactive()

