import base64
import sys
import cbor2
import json

def decode_base64_and_parse_cbor(filename):
    # Step 1: Decode base64 and save to file
    with open(filename, 'r') as f:
        base64_str = f.read().strip()
        decoded_bytes = base64.b64decode(base64_str)
        with open('decoded.bin', 'wb') as out_bin:
            out_bin.write(decoded_bytes)
        print("Base64-decoded bytes saved to decoded.bin")

    # Step 2: Parse as CBOR and save as JSON
    try:
        cbor_obj = cbor2.loads(decoded_bytes)
        with open('decoded.json', 'w') as out_json:
            json.dump(cbor_obj, out_json, indent=2, ensure_ascii=False)
        print("CBOR-decoded data saved to decoded.json")
    except Exception as e:
        print(f"Error decoding CBOR: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_cbor.py <base64_file>")
        sys.exit(1)
    decode_base64_and_parse_cbor(sys.argv[1]) 