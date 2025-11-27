import json
import serial
import time
import os

# -------------------- CONFIG --------------------
JSON_PATH = r"connection\sample_bit_hex.json"
SERIAL_PORT = "COM3"     # change to your actual COM port
BAUD_RATE = 115200         # must match your microcontroller
SYNC_BYTE = b'\xFF'      # 0xFF sync byte in binary
# ------------------------------------------------


def send_binary_string(ser, binary_str):
    """
    Convert a binary string (e.g., '01001100') into a byte and send over serial.
    Pads automatically if length is not multiple of 8.
    """
    # clean and pad
    binary_str = binary_str.strip()
    if len(binary_str) % 8 != 0:
        binary_str = binary_str.zfill(8 - (len(binary_str) % 8) + len(binary_str))

    # split into 8-bit chunks
    for i in range(0, len(binary_str), 8):
        chunk = binary_str[i:i+8]
        byte_val = int(chunk, 2)
        ser.write(byte_val.to_bytes(1, byteorder='big'))
        time.sleep(0.05)  # small delay for MCU to process


def transmit_json_data(json_path):
    """Read JSON and send each step’s binary data over serial."""
    if not os.path.isfile(json_path):
        print(f"❌ File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Connect to serial port
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow time for connection
        print(f"✅ Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"❌ Serial connection failed: {e}")
        return

    # Recursive function to find and send any binary pairs
    def process_dict(d):
        if isinstance(d, dict):
            if "step_name" in d and "purge" in d:
                # Send sync
                ser.write(SYNC_BYTE)
                print("↪ Sent sync (0xFF)")

                # Send step_name
                step_bits = d["step_name"]
                purge_bits = d["purge"]

                send_binary_string(ser, step_bits)
                print(f"↪ Sent step_name: {step_bits}")

                send_binary_string(ser, purge_bits)
                print(f"↪ Sent purge: {purge_bits}")

            # Process nested dicts or lists
            for val in d.values():
                process_dict(val)
        elif isinstance(d, list):
            for item in d:
                process_dict(item)

    # Start sending
    process_dict(data)

    ser.close()
    print("✅ Transmission complete & serial port closed.")


if __name__ == "__main__":
    transmit_json_data(JSON_PATH)
