import fs
import random as rd

if __name__ == '__main__':
    storage = fs.Storage(2 ** 6)
    storage.create_file(fs.Path("random"))
    for i in range(40):
        s = b""
        for i in range(rd.randint(4, 5)):
            s += rd.choice([b"A", b"B", b"C", b"D"])
        storage.edit_file(fs.Path("random"), s)
        print(storage.bytes)
        print(s)
