import cbor2

CBOR_FILE = 'agecbor'

def main():
    try:
        with open(CBOR_FILE, 'rb') as f:
            cbor_data = f.read()
        obj = cbor2.loads(cbor_data)
        print("CBOR parsing succeeded.")
    except Exception as e:
        print(f"CBOR parsing failed: {e}")

if __name__ == '__main__':
    main() 