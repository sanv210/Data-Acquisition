import json
import os
# If dictionary.py is not in the same directory, uncomment below lines and set correct path:
# import sys
# sys.path.append(r"C:\Users\jhaad\Downloads\DAQ_Project\connection")

from dictionary import BITSTREAM_MAP


def num_to_byte_binary(num):
    """Divide by 10 and return an 8-bit binary string."""
    try:
        scaled = int(float(num) / 10)
        binary = format(scaled, '08b')  # ensures 8-bit binary
        return binary
    except Exception:
        return str(num)  # fallback for safety


def value_to_hex_or_bit(value):
    """Convert strings to hex, dictionary-mapped to bitstream, numbers to 8-bit binary."""
    if isinstance(value, str):
        # If matches dictionary, replace with bitstream
        return BITSTREAM_MAP.get(value, value.encode('utf-8').hex())
    elif isinstance(value, (int, float)):
        return num_to_byte_binary(value)
    elif isinstance(value, list):
        return [value_to_hex_or_bit(v) for v in value]
    elif isinstance(value, dict):
        return convert_json_to_bit_hex(value)
    else:
        return value


def convert_json_to_bit_hex(data):
    """Recursively convert JSON values."""
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                new_dict[key] = convert_json_to_bit_hex(value)
            else:
                new_dict[key] = value_to_hex_or_bit(value)
        return new_dict

    elif isinstance(data, list):
        return [convert_json_to_bit_hex(item) for item in data]

    else:
        return value_to_hex_or_bit(data)


def json_payload_to_bit_hex(file_path):
    """Main function to load JSON, convert, and save."""
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converted_data = convert_json_to_bit_hex(data)

    base, _ = os.path.splitext(file_path)
    output_path = f"{base}_bit_hex.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=4)

    print(f"✅ Converted JSON saved as: {output_path}")


if __name__ == "__main__":
    destination_json = r"connection\sample.json"
    json_payload_to_bit_hex(destination_json)
