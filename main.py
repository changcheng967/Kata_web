import os
import subprocess
import requests
import zipfile
import shutil

# Constants
libzip_url = "http://archive.ubuntu.com/ubuntu/pool/universe/libz/libzip/libzip5_1.5.1-0ubuntu1_amd64.deb"
libssl_url = "http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb"
libzip_deb = "libzip5_1.5.1-0ubuntu1_amd64.deb"
libssl_deb = "libssl1.1_1.1.1f-1ubuntu2_amd64.deb"
lib_dir = "libs"

katago_url = "https://github.com/lightvector/KataGo/releases/download/v1.15.3/katago-v1.15.3-eigen-linux-x64.zip"
katago_zip = "katago-v1.15.3-eigen-linux-x64.zip"
katago_dir = "katago"
model_url = "https://github.com/changcheng967/Kata_web/releases/download/v1.1/final_model.bin"
model_bin = "final_model.bin"

cgos_client_url = "https://github.com/zakki/cgos/releases/download/v1.1.0/cgos-client-python-v1.1.0.zip"
cgos_zip = "cgos-client-python-v1.1.0.zip"
cgos_dir = "cgos_client"

# CGOS connection info
CGOS_SERVER = "g0.cgos.go.jp"
CGOS_PORT = "6809"
BOT_NAME = "KataWeb"
BOT_PASSWORD = "142857"
BOARD_SIZE = "9"
KOMI = "7.5"

# --- Step 1: Download and extract libzip5 and libssl1.1 ---
print("Downloading libzip5 and libssl1.1...")

os.makedirs(lib_dir, exist_ok=True)

for url, deb in [(libzip_url, libzip_deb), (libssl_url, libssl_deb)]:
    try:
        print(f"Downloading {deb}...")
        response = requests.get(url)
        with open(deb, "wb") as f:
            f.write(response.content)
        print(f"Extracting {deb}...")
        subprocess.run(["dpkg-deb", "-x", deb, lib_dir], check=True)
        os.remove(deb)
        print(f"Deleted {deb}.")
    except Exception as e:
        print(f"Error processing {deb}: {e}")

libzip_lib_path = os.path.join(lib_dir, "usr", "lib", "x86_64-linux-gnu")
libssl_lib_path = os.path.join(lib_dir, "lib", "x86_64-linux-gnu")
os.environ["LD_LIBRARY_PATH"] = f"{libzip_lib_path}:{libssl_lib_path}"
print("Library paths set.")

# --- Step 2: Download and unzip KataGo (Eigen version) ---
print("Downloading KataGo (Eigen version)...")
try:
    response = requests.get(katago_url)
    with open(katago_zip, "wb") as f:
        f.write(response.content)
    with zipfile.ZipFile(katago_zip, "r") as zip_ref:
        zip_ref.extractall(katago_dir)
    os.remove(katago_zip)
    katago_exec_path = os.path.join(katago_dir, "katago")
    os.chmod(katago_exec_path, 0o755)
    print("KataGo setup complete.")
except Exception as e:
    print(f"Error setting up KataGo: {e}")

# --- Step 3: Download KataGo model (final_model.bin) ---
print("Downloading KataGo model (final_model.bin)...")
try:
    response = requests.get(model_url)
    with open(os.path.join(katago_dir, model_bin), "wb") as f:
        f.write(response.content)
    print("KataGo model setup complete.")
except Exception as e:
    print(f"Error setting up KataGo model: {e}")

# --- Step 4: Download and extract CGOS client python zip ---
print("Downloading CGOS client python zip...")
try:
    response = requests.get(cgos_client_url)
    with open(cgos_zip, "wb") as f:
        f.write(response.content)
    if os.path.exists(cgos_dir):
        shutil.rmtree(cgos_dir)
    with zipfile.ZipFile(cgos_zip, "r") as zip_ref:
        # Extract the inner folder cgos-client-python-v1.1.0 inside the zip as root
        # The zip has a root folder named cgos-client-python-v1.1.0, so extract with that in mind
        for member in zip_ref.namelist():
            # Extract to cgos_client/, removing the top-level folder prefix
            filename = member
            if member.startswith("cgos-client-python-v1.1.0/"):
                filename = member[len("cgos-client-python-v1.1.0/"):]
            if filename:
                dest = os.path.join(cgos_dir, filename)
                if member.endswith("/"):
                    os.makedirs(dest, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "wb") as outfile:
                        outfile.write(zip_ref.read(member))
    os.remove(cgos_zip)
    print("CGOS client setup complete.")
except Exception as e:
    print(f"Error setting up CGOS client: {e}")

# --- Step 5: Create Minimal GTP Config for KataGo ---
print("Creating minimal GTP config for KataGo...")
minimal_gtp_cfg_path = os.path.join(katago_dir, "cgos_gtp.cfg")
try:
    with open(minimal_gtp_cfg_path, "w") as f:
        f.write(f"""logSearchInfo = false
maxTime = 1.0
model = {os.path.join(katago_dir, model_bin)}
rules = tromp-taylor
""")
    print("Minimal GTP config created.")
except Exception as e:
    print(f"Error creating minimal GTP config: {e}")

# Step 6: Create CGOS client config file
print("Creating CGOS client config file...")

katago_exec_path = os.path.join(katago_dir, "katago")
minimal_gtp_cfg_path = os.path.join(katago_dir, "cgos_gtp.cfg")

# Debug print and sanity check
print("Katago executable path:", katago_exec_path)
print("Minimal GTP config path:", minimal_gtp_cfg_path)

import sys
if not os.path.exists(katago_exec_path):
    print(f"Error: KataGo executable not found at {katago_exec_path}")
    sys.exit(1)
if not os.path.exists(minimal_gtp_cfg_path):
    print(f"Error: Minimal GTP config not found at {minimal_gtp_cfg_path}")
    sys.exit(1)

try:
    config_path = os.path.join(cgos_dir, "config.cfg")
    with open(config_path, "w") as f:
        f.write(f"""[common]
name = {BOT_NAME}
password = {BOT_PASSWORD}
server = {CGOS_SERVER}
port = {CGOS_PORT}

[engine]
name = katago
command = {katago_exec_path} gtp -model {os.path.join(katago_dir, model_bin)} -config {minimal_gtp_cfg_path}
boardsize = {BOARD_SIZE}
komi = {KOMI}
""")

    print(f"CGOS config file created at '{config_path}'.")
    
    # Print out config for debugging
    with open(config_path, "r") as f:
        print("=== CGOS client config.cfg content ===")
        print(f.read())
        print("=== End of config.cfg ===")

except Exception as e:
    print(f"Error creating CGOS config file: {e}")
    sys.exit(1)


# --- Step 7: Run CGOS client ---
print("Launching KataGo on CGOS via CGOS client...")
try:
    cgos_client_script = os.path.join(cgos_dir, "bin", "cgosclient.py")
    if not os.path.exists(cgos_client_script):
        raise FileNotFoundError(f"CGOS client script not found at {cgos_client_script}")

    command = [
        "python3",
        cgos_client_script,
        config_path
    ]

    subprocess.run(command, check=True)
except Exception as e:
    print(f"Error running KataGo on CGOS: {e}")
