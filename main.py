from lexer import Lexer

a = Lexer()

for e in a:
    print(e)

print(a.literals)
print(a.ids)
