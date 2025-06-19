import sys
import requests
from tqdm import tqdm
import os

def upload_to_gofile(file_path):
    # Step 1: Get best server
    server_response = requests.get("https://api.gofile.io/servers").json()
    server = server_response["data"]["servers"][0]["name"]

    # Step 2: Upload file
    with open(file_path, 'rb') as f:
        file_size = os.path.getsize(file_path)
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as progress_bar:
            def progress_monitor(chunk):
                progress_bar.update(len(chunk))

            response = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={"file": (os.path.basename(file_path), f)},
                stream=True
            )

    upload_data = response.json()
    link = upload_data["data"]["downloadPage"]
    print(link)
    print()  # Blank line for readability

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No File Specified!")
        sys.exit(1)
    upload_to_gofile(sys.argv[1])
