import os
import subprocess
import requests
import zipfile
import gzip
import shutil
import json

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
        subprocess.run(["dpkg-deb", "-x", deb, lib_dir])
        if os.path.exists(deb):
            os.remove(deb)
            print(f"Deleted {deb}.")
    except Exception as e:
        print(f"Error processing {deb}: {e}")

libzip_lib_path = os.path.join(lib_dir, "usr", "lib", "x86_64-linux-gnu")
libssl_lib_path = os.path.join(lib_dir, "lib", "x86_64-linux-gnu")
os.environ["LD_LIBRARY_PATH"] = f"{libzip_lib_path}:{libssl_lib_path}"

# Step 2: Download and unzip KataGo (Eigen version)
print("Downloading KataGo (Eigen version)...")
katago_url = "https://github.com/lightvector/KataGo/releases/download/v1.16.3/katago-v1.16.3-cuda12.5-cudnn8.9.7-linux-x64.zip"
katago_zip = "katago-v1.16.3-cuda12.5-cudnn8.9.7-linux-x64.zip"
katago_dir = "katago"

try:
    print(f"Downloading {katago_zip}...")
    response = requests.get(katago_url)
    with open(katago_zip, "wb") as f:
        f.write(response.content)
    print(f"Extracting {katago_zip}...")
    with zipfile.ZipFile(katago_zip, "r") as zip_ref:
        zip_ref.extractall(katago_dir)
    if os.path.exists(katago_zip):
        os.remove(katago_zip)
        print(f"Deleted {katago_zip}.")
    os.chmod(os.path.join(katago_dir, "katago"), 0o755)
    print("KataGo setup complete.")
except Exception as e:
    print(f"Error setting up KataGo: {e}")

# Step 3: Download the KataGo model
print("Downloading KataGo model...")
model_url = "https://github.com/changcheng967/Kata_web/releases/download/KW-20250919-b18c384nbt-71k-9x9-final/KW-20250919-b18c384nbt-71k-9x9-final.bin"
model_bin = "KW-20250919-b18c384nbt-71k-9x9-final.bin"

try:
    print(f"Downloading {model_gz}...")
    response = requests.get(model_url)
    with open(model_gz, "wb") as f:
        f.write(response.content)
    print(f"Extracting {model_gz}...")
    with gzip.open(model_gz, "rb") as gz_file:
        with open(os.path.join(katago_dir, model_bin), "wb") as bin_file:
            shutil.copyfileobj(gz_file, bin_file)
    if os.path.exists(model_gz):
        os.remove(model_gz)
        print(f"Deleted {model_gz}.")
    print("KataGo model setup complete.")
except Exception as e:
    print(f"Error setting up KataGo model: {e}")

# Step 4: Download gtp2ogs
print("Downloading gtp2ogs...")
gtp2ogs_url = "https://github.com/online-go/gtp2ogs/releases/download/9.0/gtp2ogs-9.0.0-linux"
gtp2ogs_binary = "gtp2ogs"

try:
    print(f"Downloading {gtp2ogs_binary}...")
    response = requests.get(gtp2ogs_url)
    with open(gtp2ogs_binary, "wb") as f:
        f.write(response.content)
    os.chmod(gtp2ogs_binary, 0o755)
    print("gtp2ogs setup complete.")
except Exception as e:
    print(f"Error setting up gtp2ogs: {e}")

# Step 5: Modify default_gtp.cfg
print("Updating default_gtp.cfg...")
default_gtp_cfg_path = os.path.join(katago_dir, "default_gtp.cfg")

try:
    with open(default_gtp_cfg_path, "r") as f:
        lines = f.readlines()

    # Apply the original changes
    lines[54] = "logSearchInfo = true\n"
    lines[63] = "ogsChatToStderr = True\n"
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
        "# scoringRule = TERRITORY  # Territory scoring (special computer-friendly territory rules)\n",
        "\n",
        "taxRule = NONE  # All surrounded empty points are scored\n",
        "# taxRule = SEKI  # Eyes in seki do NOT count as points\n",
        "# taxRule = ALL   # All groups are taxed up to 2 points for the two eyes needed to live\n",
        "\n",
        "# Is multiple-stone suicide legal? (Single-stone suicide is always illegal).\n",
        "# multiStoneSuicideLegal = false\n",
        "multiStoneSuicideLegal = true  # Allow multi-stone suicide\n",
        "\n",
        "# \"Button go\" - the first pass when area scoring awards 0.5 points and does\n",
        "# not count for ending the game.\n",
        "# Allows area scoring rulesets that have far simpler rules to achieve the same\n",
        "# final scoring precision and reward for precise play as territory scoring.\n",
        "# hasButton = false\n",
        "# hasButton = true\n",
        "\n",
        "# Is this a human ruleset where it's okay to pass before having physically\n",
        "# captured and removed all dead stones?\n",
        "# friendlyPassOk = false\n",
        "friendlyPassOk = true  # Allow friendly pass\n",
        "\n",
        "# How handicap stones in handicap games are compensated\n",
        "# whiteHandicapBonus = 0    # White gets no compensation for black's handicap stones (Tromp-taylor, NZ, JP)\n",
        "# whiteHandicapBonus = N-1  # White gets N-1 points for black's N handicap stones (AGA)\n",
        "# whiteHandicapBonus = N    # White gets N points for black's N handicap stones (Chinese)\n",
    ]

    # Write the updated content back to the file
    with open(default_gtp_cfg_path, "w") as f:
        f.writelines(lines)
    print("default_gtp.cfg has been updated successfully!")
except Exception as e:
    print(f"Error updating default_gtp.cfg: {e}")

# Step 6: Generate kata_speed.json5
print("Generating kata_speed.json5...")
kata_speed_config = {
    "blacklist": ["Tilano", "ujykfyijhgf", "Benneviss", "world2049", "extoom"],
    "whitelist": ["xqqzldh", "Golaxy 9D", "俱乐部AI", "Doudoubot", "Katagui40b", "Kata_speed"],
    "allow_ranked": True,
    "decline_new_challenges": False,
    "max_games_per_player": 1,
    "hidden": False,
    "allowed_board_sizes": [9, 13, 19],
    "engine": "KataGo b18 network with usually only 7 visits, takes about 3-5 seconds per move.",
    "allow_unranked": True,
    "farewellscore": True,
    "bot": {
        "send_pv_data": True,
        "send_chats": True
    },
    # Disable correspondence games
    "allowed_correspondence_settings": None
}

try:
    with open("kata_speed.json5", "w", encoding="utf-8") as f:
        json.dump(kata_speed_config, f, indent=4, ensure_ascii=False)
    print("kata_speed.json5 has been generated successfully!")
except Exception as e:
    print(f"Error generating kata_speed.json5: {e}")

# Step 7: Run gtp2ogs with KataGo
print("Running gtp2ogs with KataGo...")
api_key = "your-api-key"
command = [
    "./gtp2ogs",
    "--apikey", api_key,
    "--config", "kata_speed.json5",
    "--",
    os.path.join(katago_dir, "katago"),
    "gtp",
    "-config", os.path.join(katago_dir, "default_gtp.cfg"),
    "-model", os.path.join(katago_dir, model_bin)
]

try:
    subprocess.run(command)
except Exception as e:
    print(f"Error running gtp2ogs: {e}")
