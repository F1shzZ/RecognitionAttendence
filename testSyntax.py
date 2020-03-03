class a():
    a = 'a'
    c = 'c'
    def __init__(self):
        self.b = 'b'

    def change(self):
        self.K = 'K'
        self.a = 'A'
        a.c = 'C'

    @classmethod
    def get(cls):
        return cls.c
        
B = a()

A = a()
print(A.a, A.b, A.get(), A.c)
print(B.a, B.b, B.get(), B.c)

# A.a = 'A'
A.b = 'B'
print(A.a, A.b)

print(B.a, B.b)

B.change()

print(A.a, A.b, A.get(), A.c)
print(B.a, B.b, B.get(), B.c, B.K)
