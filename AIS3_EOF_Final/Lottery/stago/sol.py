with open('flag.png', 'rb') as f:
    data = f.read()

print(data)

with open('out', 'wb') as file:
    file.write(data)