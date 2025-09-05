import os
import subprocess
import requests
import zipfile
import shutil

# Step 1: Download and extract libzip5 and libssl1.1
print("Downloading libzip5 and libssl1.1...")
libzip_url = "http://archive.ubuntu.com/ubuntu/pool/universe/libz/libzip/libzip5_1.5.1-0ubuntu1_amd64.deb"
libssl_url = "http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb"
libzip_deb = "libzip5_1.5.1-0ubuntu1_amd64.deb"
libssl_deb = "libssl1.1_1.1.1f-1ubuntu2_amd64.deb"
lib_dir = "libs"

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

# Step 2: Download and unzip KataGo (Eigen version)
print("Downloading KataGo (Eigen version)...")
katago_url = "https://github.com/lightvector/KataGo/releases/download/v1.15.3/katago-v1.15.3-eigen-linux-x64.zip"
katago_zip = "katago-v1.15.3-eigen-linux-x64.zip"
katago_dir = "katago"

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

# Step 3: Download KataGo model (final_model.bin)
print("Downloading KataGo model (final_model.bin)...")
model_url = "https://github.com/changcheng967/Kata_web/releases/download/v1.1/final_model.bin"
model_bin = "final_model.bin"
model_path = os.path.join(katago_dir, model_bin)

try:
    response = requests.get(model_url)
    with open(model_path, "wb") as f:
        f.write(response.content)
    print("KataGo model setup complete.")
except Exception as e:
    print(f"Error setting up KataGo model: {e}")

# Step 4: Download and extract CGOS client python zip
print("Downloading CGOS client python zip...")
cgos_client_url = "https://github.com/zakki/cgos/releases/download/v1.1.0/cgos-client-python-v1.1.0.zip"
cgos_zip = "cgos-client-python-v1.1.0.zip"
cgos_dir = "cgos_client"

try:
    response = requests.get(cgos_client_url)
    with open(cgos_zip, "wb") as f:
        f.write(response.content)

    # Remove existing folder before extraction
    if os.path.exists(cgos_dir):
        shutil.rmtree(cgos_dir)

    with zipfile.ZipFile(cgos_zip, "r") as zip_ref:
        zip_ref.extractall(cgos_dir)

    os.remove(cgos_zip)
    print("CGOS client setup complete.")

    # Adjust cgos_dir to nested folder inside the extracted dir
    cgos_dir = os.path.join(cgos_dir, "cgos-client-python-v1.1.0")
except Exception as e:
    print(f"Error setting up CGOS client: {e}")


# Step 5: Create minimal GTP config for KataGo
print("Creating minimal GTP config for KataGo...")
minimal_gtp_cfg_path = os.path.join(katago_dir, "cgos_gtp.cfg")

try:
    with open(minimal_gtp_cfg_path, "w") as f:
        f.write(f"""logSearchInfo = false
maxTime = 1.0
model = {model_path}
rules = tromp-taylor
""")
    print("Minimal GTP config created.")
except Exception as e:
    print(f"Error creating GTP config: {e}")

# Step 6: Create CGOS client config file
print("Creating CGOS client config file...")
cgos_config_path = os.path.join(cgos_dir, "config.cfg")

try:
    with open(cgos_config_path, "w") as f:
        f.write(f"""server = g0.cgos.go.jp
port = 6809
name = KataWeb
password = 142857
exec = {katago_exec_path} gtp -model {model_path} -config {minimal_gtp_cfg_path}
boardsize = 9
komi = 7.5
""")
    print(f"CGOS config file created at '{cgos_config_path}'.")
except Exception as e:
    print(f"Error creating CGOS config file: {e}")

# Step 7: Run CGOS client
print("Launching KataGo on CGOS via CGOS client...")

cgos_client_script = os.path.join(cgos_dir, "bin", "cgosclient.py")

if not os.path.exists(cgos_client_script):
    print(f"CGOS client script not found at {cgos_client_script}")
else:
    command = ["python3", cgos_client_script, cgos_config_path]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running CGOS client: {e}")
