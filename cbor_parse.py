import base64
import sys
import cbor2
import json
from hashlib import sha256
import datetime
from typing import Any, Dict, List, Union

def format_value(value: Any) -> str:
    """Format a value for display, handling special cases."""
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return f"<binary data: {value.hex()}>"
    elif isinstance(value, datetime.datetime):
        return value.isoformat()
    return str(value)

def parse_cbor_tag(tag: cbor2.CBORTag, depth: int = 0) -> Dict[str, Any]:
    """Parse a CBOR tag and its value."""
    indent = '  ' * depth
    result = {
        'tag': tag.tag,
        'value': None
    }
    
    if tag.tag == 24:  # Special handling for tag 24 (embedded CBOR)
        try:
            embedded = cbor2.loads(tag.value)
            result['value'] = parse_value(embedded, depth + 1)
        except Exception as e:
            result['value'] = f"Error parsing embedded CBOR: {e}"
    else:
        result['value'] = parse_value(tag.value, depth + 1)
    
    return result

def parse_value(value: Any, depth: int = 0) -> Union[Dict, List, str, Any]:
    """Parse a CBOR value and return a structured representation."""
    if isinstance(value, cbor2.CBORTag):
        return parse_cbor_tag(value, depth)
    elif isinstance(value, dict):
        return {format_value(k): parse_value(v, depth + 1) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [parse_value(item, depth + 1) for item in value]
    elif isinstance(value, bytes):
        try:
            return parse_value(cbor2.loads(value), depth)
        except Exception:
            return format_value(value)
    else:
        return format_value(value)

def parse(data: bytes, depth: int = 0) -> Dict[str, Any]:
    """Main parsing function that handles the CBOR data."""
    try:
        obj = cbor2.loads(data)
        return parse_value(obj, depth)
    except Exception as e:
        print(f"Error parsing CBOR data: {e}")
        print(f"Raw hex: {data.hex()}")
        return {"error": str(e), "raw_hex": data.hex()}

def main(filename: str) -> None:
    """Main function to read and parse a CBOR file."""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        result = parse(data)
        
        # Save the parsed result to a JSON file for easier inspection
        output_file = f"{filename}.txt"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Parsed CBOR data saved to {output_file}")
        
        # Print a summary of the parsed data
        print("\nParsed CBOR Structure:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mycbor2.py <cbor_file>")
        sys.exit(1)
    main(sys.argv[1])