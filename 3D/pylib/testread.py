with open('pointcl.ply') as f:
    i = 00
    line = f.readline(i)
    while i < 20:
        line = f.readline(i)
        i += 1
        print(line)