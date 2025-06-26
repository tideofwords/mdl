import base64
import sys
import cbor2
import json
from hashlib import sha256
import datetime


def parse(data, depth = 0):
    if isinstance(data, cbor2.CBORTag):
        print(f"{'  ' * depth}CBORTag {data.tag}")
        parse(data.value, depth + 1)
        return
    if isinstance(data, bytes):
        try:
            obj = cbor2.loads(data)
            print(f"{'  ' * (depth )}Parsed {len(data)} bytes to object of type {type(obj)}")
            if isinstance(obj, cbor2.CBORTag):
                print(sha256(data).hexdigest())
            if len(data) == 64:
                print(f"{'  ' * (depth )}Parsed bytes: {hex(data)}")
        except Exception as e:
            print(f"{'  ' * (depth )}Error parsing data: {e}")
            print(f"The hex is: {data.hex()}")
            return
    else:
        obj = data
    print(f"{'  ' * depth}Parsing object of type {type(obj)}")
    if isinstance(obj, dict):
        print(f"{'  ' * depth}'dict' of length {len(obj)}")
        for k, v in obj.items():
            print(f"{'  ' * (depth )}Key: {k}, Value of type {type(v)}")
            v_bytes = cbor2.dumps(v)
            print(f"{'  ' * (10)}Hash: {sha256(v_bytes).hexdigest()}")
            print(f"{'  ' * (10)}Length of thing hashed: {len(v_bytes)}")
            if type(v) == bytes:
                print(f"{'  ' * (10)}Bytes: {v.hex()}")
            parse(v, depth + 1)
    elif isinstance(obj, (list, tuple)):
        print(f"{'  ' * depth}{'list' if isinstance(obj, list) else 'tuple'} of length {len(obj)}")
        for i, item in enumerate(obj):
            print(f"{'  ' * (depth )}Item {i}:")
            parse(item, depth + 1)
    elif isinstance(obj, int):
        print(f"{'  ' * (depth )}Int: {obj}")
    elif isinstance(obj, str):
        print(f"{'  ' * (depth )}String: {obj}")
    elif isinstance(obj, cbor2.CBORTag):
        print(f"{'  ' * depth}CBORTag: {obj.tag}")
        parse(obj.value, depth + 1)
    elif isinstance(obj, datetime.datetime):
        print(f"{'  ' * (depth )}DateTime: {obj}")


    return


def main(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    parse(data)

if __name__ == "__main__":
    main("decoded.bin")