import base64
import cbor2
import datetime

CBOR_FILE = 'cbor'
OUTPUT_FILE = 'cbor_pretty.txt'
MAX_BYTES_DISPLAY = 1000


def pretty_print(obj, file, indent=0):
    prefix = ' ' * indent
    if isinstance(obj, dict):
        file.write(f'{prefix}dict {{\n')
        for k, v in obj.items():
            file.write(f'{prefix}  {repr(k)}: ')
            pretty_print(v, file, indent + 4)
        file.write(f'{prefix}}}\n')
    elif isinstance(obj, (list, tuple)):
        tname = 'list' if isinstance(obj, list) else 'tuple'
        file.write(f'{prefix}{tname} [\n')
        for i, item in enumerate(obj):
            file.write(f'{prefix}  {i}: ')
            pretty_print(item, file, indent + 4)
        file.write(f'{prefix}]\n')
    elif isinstance(obj, bytes):
        if len(obj) > MAX_BYTES_DISPLAY:
            hexstr = obj[:MAX_BYTES_DISPLAY].hex()
            file.write(f'<bytes {len(obj)} bytes, first {MAX_BYTES_DISPLAY} as hex: {hexstr}...>\n')
        else:
            hexstr = obj.hex()
            file.write(f'<bytes {len(obj)} bytes, hex: {hexstr}>\n')
    elif isinstance(obj, datetime.datetime):
        file.write(f'<datetime {obj.isoformat()}>\n')
    elif isinstance(obj, cbor2.CBORTag):
        file.write(f'<CBORTag {obj.tag}:\n')
        pretty_print(obj.value, file, indent + 4)
        file.write(f'{prefix}>\n')
    else:
        file.write(f'{repr(obj)}\n')


def main():
    # Read the base64-encoded data from the file
    with open(CBOR_FILE, 'r') as f:
        base64_data = f.read().strip()

    # Decode the base64 data
    decoded_data = base64.b64decode(base64_data)

    # Parse the CBOR data
    obj = cbor2.loads(decoded_data)

    # Pretty-print to file
    with open(OUTPUT_FILE, 'w') as f:
        pretty_print(obj, f)

if __name__ == '__main__':
    main() 