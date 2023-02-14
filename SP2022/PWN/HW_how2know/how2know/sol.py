from pwn import *

#context.arch = 'amd64'
#context.terminal = ['tmux','splitw','-h']
#r = remote('edu-ctf.zoolab.org', 10002)


#先找 overflow offset 
padding = "A"*0x18

#找出 flag 的相對位址
#&flag

#byte by byte 的爆出 flag
'''
for i in range(126):
    for j in range(30):

        if flag[j] == chr(j):
            r = process('/ctf/work/SP2022/hw_how2know/share/chal')
            print(f"string ", i ," is ",chr(i))
            sleep(1.5)
        else:
    
'''
payload = asm('mov eax, 0')
print(payload)


#Payload = padding

#r.sendlineafter(b'talk is cheap, show me the code\n', Payload)



'''
ba = bytearray.fromhex('7365547b47414c460a7d74')
ba.reverse()
print(bytearray.fromhex(ba.hex()).decode('utf-8'))
'''




int main() {
    if flag[j] == chr(j):
        r = process('/ctf/work/SP2022/hw_how2know/share/chal')
        print(f"string ", i ," is ",chr(i))
        sleep(1.5)
    ＝else:
    
}