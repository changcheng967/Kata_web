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

KATAGO_URL = "https://github.com/lightvector/KataGo/releases/download/v1.16.3/katago-v1.16.3-eigen-linux-x64.zip"
KATAGO_ZIP = os.path.join(WORK_DIR, "katago.zip")
KATAGO_DIR = os.path.join(WORK_DIR, "katago")
KATAGO_EXEC = os.path.join(KATAGO_DIR, "katago")
KATAGO_MODEL_URL = "https://github.com/changcheng967/Kata_web/releases/download/v1.1/final_model.bin"
KATAGO_MODEL_BIN = os.path.join(WORK_DIR, "final_model.bin")

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
# Required logging keys
logAllGTPCommunication = false
logSearchInfo = false
logPolicy = false
logPolicyTarget = false
logValue = false
logOwnership = false
logPV = false

# Basic limits
maxVisits = 1
maxPlayouts = 100
maxTime = 0

# Optional but safe
numSearchThreads = 2
searchBatchSize = 1
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
"""
    with open(path, "w") as f:
        f.write(config_content.strip() + "\n")
    print(f"CGOS client config created at {path}")

def find_cgosclient_script(cgos_client_dir):
    for root, _, files in os.walk(cgos_client_dir):
        if "cgosclient.py" in files:
            return os.path.join(root, "cgosclient.py")
    return None

# === Main script ===

def main():
    # Download and extract KataGo
    if not os.path.isfile(KATAGO_EXEC):
        download_file(KATAGO_URL, KATAGO_ZIP)
        os.makedirs(KATAGO_DIR, exist_ok=True)
        extract_zip(KATAGO_ZIP, KATAGO_DIR)
        os.remove(KATAGO_ZIP)
    # Make sure the binary is executable
        os.chmod(KATAGO_EXEC, 0o755)
        if not os.path.isfile(KATAGO_EXEC):
            print("Error: KataGo executable not found after extraction.")
            sys.exit(1)
        print(f"KataGo downloaded and extracted to {KATAGO_DIR}")
    else:
        print(f"KataGo executable already exists: {KATAGO_EXEC}")

    # Download KataGo model
    if not os.path.isfile(KATAGO_MODEL_BIN):
        print("Downloading KataGo model...")
        download_file(KATAGO_MODEL_URL, KATAGO_MODEL_BIN)
        print(f"KataGo model downloaded to {KATAGO_MODEL_BIN}")
    else:
        print(f"KataGo model already exists: {KATAGO_MODEL_BIN}")

    # Download and extract CGOS client
    if not os.path.isdir(CGOS_CLIENT_DIR):
        download_file(CGOS_CLIENT_URL, CGOS_CLIENT_ZIP)
        extract_zip(CGOS_CLIENT_ZIP, WORK_DIR)
        outer_dir = os.path.join(WORK_DIR, "cgos-client-python-v1.1.0")
        nested_dir = os.path.join(outer_dir, "cgos-client-python-v1.1.0")
        if os.path.isdir(nested_dir):
            shutil.move(nested_dir, CGOS_CLIENT_DIR)
            shutil.rmtree(outer_dir, ignore_errors=True)
        else:
            shutil.move(outer_dir, CGOS_CLIENT_DIR)
        os.remove(CGOS_CLIENT_ZIP)
        print(f"CGOS client extracted to {CGOS_CLIENT_DIR}")
    else:
        print(f"CGOS client already exists: {CGOS_CLIENT_DIR}")

    # Create minimal GTP config
    gtp_config_path = os.path.join(KATAGO_DIR, "cgos_gtp.cfg")
    create_minimal_gtp_config(gtp_config_path)

    # Create CGOS config
    cgos_config_path = os.path.join(CGOS_CLIENT_DIR, "config.cfg")
    create_cgos_config(cgos_config_path, KATAGO_EXEC, KATAGO_MODEL_BIN, gtp_config_path, BOT_NAME, BOT_PASSWORD)

    # Find and run CGOS client
    cgosclient_py = find_cgosclient_script(CGOS_CLIENT_DIR)
    if not cgosclient_py:
        print("Error: cgosclient.py not found.")
        sys.exit(1)

    print(f"Launching CGOS client:\nCommand: python {cgosclient_py} {cgos_config_path}")
    subprocess.run([sys.executable, cgosclient_py, cgos_config_path])

if __name__ == "__main__":
    main()
