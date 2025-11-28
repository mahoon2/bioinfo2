a = input()
b = [
    a.count("A"),
    a.count("C"),
    a.count("G"),
    a.count("T")
]
print(' '.join(map(str, b)))