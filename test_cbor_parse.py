import base64
import cbor2
import json

# Read the base64-encoded data from the file
with open('cbor', 'r') as f:
    base64_data = f.read().strip()

# Decode the base64 data
decoded_data = base64.b64decode(base64_data)

# Save the decoded data to a file
with open('decoded.bin', 'wb') as f:
    f.write(decoded_data)

# Parse the CBOR data
obj = cbor2.loads(decoded_data)

# Inspect the object structure
print("\nObject type:", type(obj))
if isinstance(obj, dict):
    print("\nTop-level keys:", list(obj.keys()))
    # For each key, show the type of its value
    for key in obj.keys():
        print(f"\nKey '{key}' has value of type:", type(obj[key]))
        if isinstance(obj[key], dict):
            print(f"Subkeys of '{key}':", list(obj[key].keys()))

# 1. Convert 'id' to hex and print to a file
if isinstance(obj, dict) and 'id' in obj:
    id_hex = obj['id'].hex()
    with open('id_hex.txt', 'w') as f:
        f.write(id_hex + '\n')
    print(f"'id' as hex written to id_hex.txt: {id_hex}")
else:
    print("No 'id' key found or not a dict.")

# 2. Break down the items of 'issuer_auth'
if 'issuer_auth' in obj and isinstance(obj['issuer_auth'], list):
    print("\nissuer_auth breakdown:")
    for i, item in enumerate(obj['issuer_auth']):
        print(f"  Item {i}: type={type(item)}, value={item}")
else:
    print("No 'issuer_auth' key found or not a list.")

# 3. Print specific values from 'mso'
mso_keys = ['digestAlgorithm', 'valueDigests', 'deviceKeyInfo', 'docType', 'validityInfo']
if 'mso' in obj and isinstance(obj['mso'], dict):
    print("\nmso values:")
    for key in mso_keys:
        value = obj['mso'].get(key, None)
        print(f"  {key}: {value}")
else:
    print("No 'mso' key found or not a dict.")

def test_cbor_parse(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    try:
        obj = cbor2.loads(data)
        print("CBOR parsing succeeded.")
    except Exception as e:
        print(f"CBOR parsing failed: {e}")

if __name__ == "__main__":
    test_cbor_parse('decoded.bin') 