import base64
import sys
import cbor2
import json

def this_parse(data, depth = 0):
    obj = cbor2.loads(data)
    print(f"{'  ' * depth}Parsing object of type {type(obj)}")
    if isinstance(obj, cbor2.CBORTag):
        print(f"{'  ' * depth}CBORTag {obj.tag}")
        this_parse(obj.value, depth + 1)
        return
    if isinstance(obj, dict):
        print(f"{'  ' * depth}dict of length {len(obj)}")
        for k, v in obj.items():
            if isinstance(v, bytes):
                print(f"{'  ' * (depth + 1)}bytes of length {len(v)}")
                this_parse(v, depth + 1)
            else:
                s = str(f"{'  ' * depth}{k}: {v}")
                print(s[:200])
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