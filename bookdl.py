import os
import requests

def download_file(url, save_dir, filename=None):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # If filename is not provided, try to get it from the URL
    if not filename:
        filename = url.split("/")[-1]

    # Full path to save the file
    file_path = os.path.join(save_dir, filename)

    try:
        print(f"Downloading from: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for bad status

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"File saved to: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# Example usage
if __name__ == "__main__":
    
    
    urls = [
    "https://ncert.nic.in/textbook/pdf/cesa1dd.zip",
    "https://ncert.nic.in/textbook/pdf/desa1dd.zip",
    "https://ncert.nic.in/textbook/pdf/eesa1dd.zip"
    
    ]    
    
    
    # Directory where the file will be saved
    save_directory = "./downloads"
    
    # Optional: Specify a filename (or leave as None to auto-detect)
    filename = None
    
    for url in urls:
        download_file(url, save_directory, filename)
        print(f"Done {url}")
