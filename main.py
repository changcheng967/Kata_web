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

def patch_gtp_config(cfg_path):
    """Patch KataGo default_gtp.cfg with CGOS settings"""
    try:
        with open(cfg_path, "r") as f:
            lines = f.readlines()

        # Apply the original changes
        lines[54]  = "logSearchInfo = true\n"
        lines[63]  = "ogsChatToStderr = True\n"
        lines[300] = "# maxVisits = 500\n"
        lines[302] = "maxTime = 1.0\n"
        lines[305] = "ponderingEnabled = true\n"

        # Apply the new rules configuration (lines 113 to 149)
        lines[113:150] = [
            "# rules = tromp-taylor\n",
            "\n",
            "# By default, the \"rules\" parameter is used, but if you comment it out and\n",
            "# uncomment one option in each of the sections below, you can specify an\n",
            "# arbitrary combination of individual rules.\n",
            "\n",
            "# koRule = SIMPLE       # Simple ko rules (triple ko = no result)\n",
            "koRule = POSITIONAL   # Positional superko\n",
            "# koRule = SITUATIONAL  # Situational superko\n",
            "\n",
            "scoringRule = AREA       # Area scoring\n",
            "# scoringRule = TERRITORY  # Territory scoring\n",
            "\n",
            "taxRule = NONE  # All surrounded empty points are scored\n",
            "# taxRule = SEKI\n",
            "# taxRule = ALL\n",
            "\n",
            "# Is multiple-stone suicide legal?\n",
            "# multiStoneSuicideLegal = false\n",
            "multiStoneSuicideLegal = true  # Allow multi-stone suicide\n",
            "\n",
            "# \"Button go\"\n",
            "# hasButton = false\n",
            "# hasButton = true\n",
            "\n",
            "# Is this a human ruleset where it's okay to pass before removing all dead stones?\n",
            "# friendlyPassOk = false\n",
            "friendlyPassOk = true  # Allow friendly pass\n",
            "\n",
            "# Handicap compensation\n",
            "# whiteHandicapBonus = 0\n",
            "# whiteHandicapBonus = N-1\n",
            "# whiteHandicapBonus = N\n",
        ]

        with open(cfg_path, "w") as f:
            f.writelines(lines)
        print(f"{cfg_path} has been updated successfully!")

    except Exception as e:
        print(f"Error updating {cfg_path}: {e}")

def create_cgos_config(path, katago_exec, model_path, gtp_config_path, bot_name, bot_password):
    config_content = f"""
Common:
  KillFile = kill.txt

GTPEngine:
  Name = KataGo
  CommandLine = {katago_exec} gtp -model {model_path} -config {gtp_config_path}
  ServerHost = yss-aya.com
  ServerPort = 6809
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
        os.chmod(KATAGO_EXEC, 0o755)
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

    # Patch KataGo default_gtp.cfg
    default_gtp_cfg_path = os.path.join(KATAGO_DIR, "default_gtp.cfg")
    cgos_gtp_cfg_path = os.path.join(KATAGO_DIR, "cgos_gtp.cfg")
    if os.path.isfile(default_gtp_cfg_path):
        shutil.copy(default_gtp_cfg_path, cgos_gtp_cfg_path)
        patch_gtp_config(cgos_gtp_cfg_path)
    else:
        print("Error: default_gtp.cfg not found in KataGo directory.")
        sys.exit(1)

    # Create CGOS config
    cgos_config_path = os.path.join(CGOS_CLIENT_DIR, "config.cfg")
    create_cgos_config(cgos_config_path, KATAGO_EXEC, KATAGO_MODEL_BIN, cgos_gtp_cfg_path, BOT_NAME, BOT_PASSWORD)

    # Find and run CGOS client
    cgosclient_py = find_cgosclient_script(CGOS_CLIENT_DIR)
    if not cgosclient_py:
        print("Error: cgosclient.py not found.")
        sys.exit(1)

    print(f"Launching CGOS client:\nCommand: python {cgosclient_py} {cgos_config_path}")
    subprocess.run([sys.executable, cgosclient_py, cgos_config_path])

if __name__ == "__main__":
    main()
