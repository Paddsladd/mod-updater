import requests
import os
from sys import exit
import hashlib
import json
from json.decoder import JSONDecodeError


config_path = "update.json"
mc_version = "26.1"
mod_loader = "fabric"
mods_folder = "mods"
hash_algorithm = "sha512" # "sha512" or "sha1"


if os.path.exists("versions"):
    installed_versions = os.listdir("versions")
    mc_version = installed_versions[0]

api = "https://api.modrinth.com/v2"
headers = {"User-Agent": "paddsladd/mod-updater/0.0.0 (info@paddsladd.com)"}
config_defaults = {"hashAlgorithm": hash_algorithm, "mcVersion": mc_version, "modLoader": mod_loader, "modsFolder": mods_folder}

def getReq(url):
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Error fetching data.")
        exit(1)
        
    return response

def postReq(url, data):
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        print("Error sending data.")
        exit(1)
        
    return response

def get_display_name(mod_id):
    response = getReq(f"{api}/project/{mod_id}")
    info = response.json()
    
    return info["title"]

def get_latest_versions(hashFiles):
    hashes = list(hashFiles.keys())
    
    data = {
        "hashes": hashes,
        "algorithm": hash_algorithm,
        "loaders": [mod_loader],
        "game_versions": [mc_version]
    }
    response = postReq(f"{api}/version_files/update", data)
    return response

def download_mod(version_data, log=False, index=0):
    file_data = version_data["files"][0]
    url = file_data["url"]
    filename = file_data["filename"]
    version = version_data["version_number"]
    project_id = version_data["project_id"]
    
    project_name = get_display_name(project_id)
    response = getReq(url)
    
    if not os.path.exists(mods_folder):
        os.makedirs(mods_folder)
    
    with open(os.path.join(mods_folder, filename), "wb") as f:
        f.write(response.content)
    
    if log and index == 0:
        print()
    if log:
        print(f"Updated \"{project_name}\" to \"{version}\"")

def sha512sum(filename):
    with open(filename, 'rb', buffering=0) as file:
        return hashlib.file_digest(file, hash_algorithm).hexdigest()

def get_mod_hashes():
    if not os.path.exists(mods_folder):
        os.makedirs(mods_folder)
    
    files = os.listdir(mods_folder)
    filterd_files = list(filter(lambda file: file.endswith(".jar"), files))
    hashes = {}
    
    for file in filterd_files:
        filepath = os.path.join(mods_folder, file)
        hash = sha512sum(filepath)
        hashes[hash] = file
    
    return hashes

def update_mods(log=False):
    hashes = get_mod_hashes()
    new_mods = get_latest_versions(hashes).json()
    mods_updated = 0
    
    for original_hash, new_version_data in new_mods.items():
        file_data = new_version_data["files"][0]
        file_path = os.path.join(mods_folder, hashes[original_hash])
        
        if original_hash == file_data["hashes"][hash_algorithm]:
            continue
        
        os.remove(file_path)
        download_mod(new_version_data, log=log, index=mods_updated)
        mods_updated += 1
        
    if log and mods_updated > 1:
        print(f"\nUpdated {mods_updated} mods!")
    elif log and mods_updated == 1:
        print(f"\nUpdated {mods_updated} mod!")
    elif log:
        print("\nAlready up to date.")

def write_default_config():
    with open(config_path, "w") as file:
        json.dump(config_defaults, file, indent=2)

def get_missing_keys():
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            missing_keys = []
            if not isinstance(config, dict): return False
            
            for key, value in config_defaults.items():
                if not key in config:
                    missing_keys.append(key)
                elif not isinstance(config[key], type(value)):
                    missing_keys.append(key)
            
            return missing_keys
    except JSONDecodeError:
        return list(config_defaults.keys())
    except FileNotFoundError:
        return list(config_defaults.keys())

def create_config():
    try:
        new_config = {}
        with open(config_path, "r") as file:
            config = json.load(file)
            if not isinstance(config, dict):
                write_default_config()
                return
            
            for key in get_missing_keys():
                config[key] = config_defaults[key]
                
            new_config = config
        
        with open(config_path, "w") as file:
            json.dump(new_config, file, indent=2)
    except JSONDecodeError:
        write_default_config()
    except FileNotFoundError:
        write_default_config()

def read_config():
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            if not isinstance(config, dict): return False
            
            for key, value in config_defaults.items():
                if not key in config:
                    return False
                
                if not isinstance(config[key], type(value)):
                    return False
            
            return config
    except JSONDecodeError:
        return False
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    config = read_config()
    if config:
        mc_version = config["mcVersion"]
        mod_loader = config["modLoader"]
        mods_folder = config["modsFolder"]
        hash_algorithm = config["hashAlgorithm"]
    else:
        create_config()
        print(f"\nCreated a config at {config_path}.")
        exit(0)
    
    update_mods(log=True)