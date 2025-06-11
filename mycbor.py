import base64
import sys
import cbor2
import json

def this_parse(data, depth = 0):
    if isinstance(data, bytes):
        obj = cbor2.loads(data)
    else:
        obj = data
    print(f"{'  ' * depth}Parsing object of type {type(obj)}")
    if isinstance(obj, cbor2.CBORTag):
        print(f"{'  ' * depth}CBORTag {obj.tag}")
        this_parse(obj.value, depth + 1)
        return
    if isinstance(obj, dict):
        print(f"{'  ' * depth}dict of length {len(obj)}")
        for k, v in obj.items():
            print(f"{'  ' * (depth)}Key: {k}")
            this_parse(v, depth + 1)
    elif isinstance(obj, (list, tuple)):
        print(f"{'  ' * depth}{'list' if isinstance(obj, list) else 'tuple'} of length {len(obj)}")
        for i, item in enumerate(obj):
            print(f"{'  ' * (depth)}Item {i}:")
            this_parse(item, depth + 1)
    elif isinstance(obj, bytes):
        print(f"{'  ' * depth}bytes: {obj.hex()}")
    else:
        s = str(f"{'  ' * depth}{obj}")
        print(s[:200])
        print(f"{'  ' * depth}This was the value")


def main(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    print("HELLO")
    print(type(data))
    this_parse(data)

if __name__ == "__main__":
    main("decoded.bin")