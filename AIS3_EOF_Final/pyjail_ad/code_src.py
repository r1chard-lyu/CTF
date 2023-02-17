open = __builtins__ . open = 0
def a():
    o = __builtins__ . open 
    x = 't'
    f = o( bytearray . fromhex ( '666'+  'c6167' ) . decode (  )  +  '.' + x + 'x' +  x ) .  read (  )  [:32]
    return f

def b(f):
    f = f . encode (  )
    g =  bytearray  (  )
    for a in f:
        g . append ( a ^ 1 )
    for i in range(__import__('random').randint(0, 1000)):
        g .  append ( __import__('random').randint(41, 126) )
    return g


def c():
    f = a (  )
    f = b ( f )
    print(f . decode (  ) )

c()