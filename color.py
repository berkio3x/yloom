import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        x= (u"\u001b[48;5;" + code + "m " + code.ljust(4))
        sys.stdout.write(x)
    print u"\u001b[0m"

