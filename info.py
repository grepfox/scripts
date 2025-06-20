import sys
import os
import hashlib
import json
import time

def generate_file_info(filepath):
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    # Ask the user for the desired output name (e.g., vayu)
    base_name = input("Enter base name for output JSON (e.g., vayu): ").strip()
    if not base_name:
        print("Error: No name provided.")
        sys.exit(1)

    output_filename = f"{base_name}.json"

    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath)

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    file_id = sha256_hash.hexdigest()

    datetime_unix = int(time.time())

    romtype = "nightly"
    version = "22.2"
    url = f"https://github.com/grepfox/ota_release/releases/download/02062025/{filename}"

    response = {
        "response": [
            {
                "datetime": datetime_unix,
                "filename": filename,
                "id": file_id,
                "romtype": romtype,
                "size": size,
                "url": url,
                "version": version
            }
        ]
    }

    with open(output_filename, "w") as json_file:
        json.dump(response, json_file, indent=2)

    print(f"OTA info has been saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file-path>")
        sys.exit(1)

    generate_file_info(sys.argv[1])