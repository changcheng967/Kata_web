import os
import sys
import shutil
import requests
import zipfile
import subprocess

# === User Config ===
BOT_NAME = "KataWeb"
BOT_PASSWORD = "142857"

WORK_DIR = os.path.abspath("cgos_workdir")
os.makedirs(WORK_DIR, exist_ok=True)

KATAGO_URL = "https://github.com/lightvector/KataGo/releases/download/v1.11.2/kataGo-v1.11.2-linux-x64.zip"
KATAGO_ZIP = os.path.join(WORK_DIR, "katago.zip")
KATAGO_DIR = os.path.join(WORK_DIR, "katago")
KATAGO_MODEL_URL = "https://github.com/lightvector/KataGo/releases/download/v1.11.2/katago_model_19b.bin.gz"
KATAGO_MODEL_GZ = os.path.join(WORK_DIR, "katago_model_19b.bin.gz")
KATAGO_MODEL_BIN = os.path.join(WORK_DIR, "final_model.bin")  # We'll rename model here

CGOS_CLIENT_URL = "https://github.com/zakki/cgos/releases/download/v1.1.0/cgos-client-python-v1.1.0.zip"
CGOS_CLIENT_ZIP = os.path.join(WORK_DIR, "cgos-client-python.zip")
CGOS_CLIENT_DIR = os.path.join(WORK_DIR, "cgos_client")

# === Helper functions ===

def download_file(url, dest):
    print(f"Downloading {url} ...")
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded to {dest}")

def extract_zip(zip_path, extract_to):
    print(f"Extracting {zip_path} to {extract_to} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction done.")

def create_minimal_gtp_config(path):
    print(f"Creating minimal GTP config at {path} ...")
    content = """
maxVisits = 1
maxPlayouts = 100
maxTime = 0
"""
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
    print("Minimal GTP config created.")

def create_cgos_config(path, katago_exec, model_path, gtp_config_path, bot_name, bot_password):
    config_content = f"""
Common:
  KillFile = kill.txt

GTPEngine:
  Name = KataGo
  CommandLine = {katago_exec} gtp -model {model_path} -config {gtp_config_path}
  ServerHost = cgos.boardspace.net
  ServerPort = 8500
  ServerUser = {bot_name}
  ServerPassword = {bot_password}
  NumberOfGames = 10
  SGFDirectory = ./sgf

#GTPObserver:
#  CommandLine = java -jar /path/to/gogui-display.jar
"""
    with open(path, "w") as f:
        f.write(config_content.strip() + "\n")
    print(f"CGOS client config created at {path}")


def find_executable_in_dir(directory, executable_name="katago"):
    # Try to find katago executable in extracted directory
    for root, _, files in os.walk(directory):
        if executable_name in files:
            return os.path.join(root, executable_name)
    return None

def find_cgosclient_script(cgos_client_dir):
    # The zip contains cgos-client-python-v1.1.0/cgos-client-python-v1.1.0/bin/cgosclient.py
    # So we look recursively for cgosclient.py
    for root, _, files in os.walk(cgos_client_dir):
        if "cgosclient.py" in files:
            return os.path.join(root, "cgosclient.py")
    return None

# === Main script ===

def main():
    # Download KataGo if needed
    if not os.path.isdir(KATAGO_DIR):
        download_file(KATAGO_URL, KATAGO_ZIP)
        extract_zip(KATAGO_ZIP, WORK_DIR)
        # The extracted folder is something like KataGo-v1.11.2-linux-x64
        # Move/rename it to KATAGO_DIR for simplicity
        extracted_folders = [f for f in os.listdir(WORK_DIR) if os.path.isdir(os.path.join(WORK_DIR, f)) and f.startswith("kataGo")]
        if not extracted_folders:
            print("Error: KataGo folder not found after extraction")
            sys.exit(1)
        shutil.move(os.path.join(WORK_DIR, extracted_folders[0]), KATAGO_DIR)
        os.remove(KATAGO_ZIP)
        print(f"KataGo downloaded and extracted to {KATAGO_DIR}")
    else:
        print(f"KataGo directory already exists: {KATAGO_DIR}")

    # Download KataGo model if needed
    if not os.path.isfile(KATAGO_MODEL_BIN):
        print("Downloading KataGo model...")
        download_file(KATAGO_MODEL_URL, KATAGO_MODEL_GZ)
        # Extract gzip
        import gzip
        with gzip.open(KATAGO_MODEL_GZ, 'rb') as f_in:
            with open(KATAGO_MODEL_BIN, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(KATAGO_MODEL_GZ)
        print(f"KataGo model extracted to {KATAGO_MODEL_BIN}")
    else:
        print(f"KataGo model already exists: {KATAGO_MODEL_BIN}")

    # Download CGOS client python zip
    if not os.path.isdir(CGOS_CLIENT_DIR):
        download_file(CGOS_CLIENT_URL, CGOS_CLIENT_ZIP)
        # The zip contains a nested folder: cgos-client-python-v1.1.0/cgos-client-python-v1.1.0/
        # Extract first, then move nested folder contents up
        extract_zip(CGOS_CLIENT_ZIP, WORK_DIR)
        outer_dir = os.path.join(WORK_DIR, "cgos-client-python-v1.1.0")
        nested_dir = os.path.join(outer_dir, "cgos-client-python-v1.1.0")
        if os.path.isdir(nested_dir):
            # Move nested_dir contents to CGOS_CLIENT_DIR
            if os.path.exists(CGOS_CLIENT_DIR):
                shutil.rmtree(CGOS_CLIENT_DIR)
            shutil.move(nested_dir, CGOS_CLIENT_DIR)
            # Remove outer dir if empty
            if os.path.isdir(outer_dir):
                try:
                    os.rmdir(outer_dir)
                except OSError:
                    pass
        else:
            # fallback - just rename outer_dir to CGOS_CLIENT_DIR
            if os.path.exists(CGOS_CLIENT_DIR):
                shutil.rmtree(CGOS_CLIENT_DIR)
            shutil.move(outer_dir, CGOS_CLIENT_DIR)

        os.remove(CGOS_CLIENT_ZIP)
        print(f"CGOS client extracted to {CGOS_CLIENT_DIR}")
    else:
        print(f"CGOS client directory already exists: {CGOS_CLIENT_DIR}")

    # Create minimal GTP config file for KataGo
    gtp_config_path = os.path.join(KATAGO_DIR, "cgos_gtp.cfg")
    if not os.path.isfile(gtp_config_path):
        create_minimal_gtp_config(gtp_config_path)
    else:
        print(f"Minimal GTP config already exists: {gtp_config_path}")

    # Find KataGo executable
    katago_exec = find_executable_in_dir(KATAGO_DIR)
    if not katago_exec:
        print("Error: KataGo executable not found")
        sys.exit(1)

    # Create CGOS client config
    cgos_config_path = os.path.join(CGOS_CLIENT_DIR, "config.cfg")
    create_cgos_config(cgos_config_path, katago_exec, KATAGO_MODEL_BIN, gtp_config_path)

    # Find cgosclient.py script
    cgosclient_py = find_cgosclient_script(CGOS_CLIENT_DIR)
    if not cgosclient_py:
        print("Error: cgosclient.py script not found")
        sys.exit(1)

    # Launch CGOS client
    print(f"Launching CGOS client...\nCommand: python {cgosclient_py} {cgos_config_path}")
    subprocess.run([sys.executable, cgosclient_py, cgos_config_path])

if __name__ == "__main__":
    main()
