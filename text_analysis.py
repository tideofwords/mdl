

def main():
    fname = "cbor_pretty"
    hashes = set()
    with open(fname, "r") as cbor_file:
        for line in cbor_file:
            if "The hex is:" in line:
                print(line[12:])

main()