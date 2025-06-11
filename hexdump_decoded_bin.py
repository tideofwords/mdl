def hexdump(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_bytes = ' '.join(f'{b:02x}' for b in chunk)
        ascii_bytes = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f'{i:08x}  {hex_bytes:<48}  {ascii_bytes}')
    
    with open(output_file, 'w') as out:
        out.write('\n'.join(lines))

if __name__ == "__main__":
    hexdump('decoded.bin', 'decoded_hexdump.txt') 