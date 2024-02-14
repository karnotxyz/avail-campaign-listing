import json
import uuid
import os
import requests
import sys

APP_CHAIN_DIRECTORY = os.path.join(os.getcwd(), "app_chains")
LISTING_JSON_LOC = os.path.join(os.getcwd(), "listing.json")
JSON_URL = "https://raw.githubusercontent.com/karnotxyz/avail-campaign-listing/main/listing.json"
TIMEOUT_IN_MS = 500


def validate_json_array(json_file):
    with open(json_file, 'r') as file:
        listing = json.load(file)

    if not isinstance(listing, list):
        print(f"Error: The JSON file {json_file} does not contain a JSON array.")
        sys.exit(1)
    return listing


def download_json_file(url):
    root_tree = requests.get(ROOT_TREE_URL, timeout=TIMEOUT_IN_MS)
    if root_tree.status_code == 200:
        root_tree = root_tree.json()
    else:
        print(f"Error: Failed to download root tree from {ROOT_TREE_URL}.")

  
def check_required_keys(obj):
    required_keys = ["id", "name", "logo", "rpc_url", "explorer_url", "metrics_endpoint"]
    for key in required_keys:
        if key not in obj:
            print(f"Error: The JSON file does not contain a {key} field.")
            sys.exit(1)
        if key == "id":
            try:
                val = uuid.UUID(obj[key])
            except Exception:
                print(f"Error: KEY provided {key} is not a valid UUID.")
                sys.exit(1)


def check_url_status_code(obj):
    try:
        if "rpc_url" in obj:
            response = requests.get(obj["rpc_url"] + "/health", timeout=TIMEOUT_IN_MS)
            if response.status_code != 200:
                print(f"Error: The RPC URL {obj['rpc_url']} is not accessible.")
                sys.exit(1)
        else:
            print(f"Error: The JSON file does not contain a rpc_url field.")
            sys.exit(1)

        if "explorer_url" in obj:
            response = requests.get(obj["explorer_url"] + "/blocks/1", timeout=TIMEOUT_IN_MS)
            if response.status_code != 200:
                print(f"Error: The Explorer URL {obj['explorer_url']} is not accessible.")
                sys.exit(1)
        else:
            print(f"Error: The JSON file does not contain a explorer_url field.")
            sys.exit(1)

        if "metrics_endpoint" in obj:
            response = requests.get(obj["metrics_endpoint"], timeout=TIMEOUT_IN_MS)
            if response.status_code != 200:
                print(f"Error: The Metrics URL {obj['metrics_endpoint']} is not accessible.")
                sys.exit(1)
        else:
            print(f"Error: The JSON file does not contain a metrics_endpoint field.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: URL not working - {e.args[0].reason.args[0]}")
        sys.exit(1)


def list_files(directory_path):
    try:
        files = os.listdir(directory_path)
        files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]

        return files
    except OSError as e:
        print(f"Error listing files in {directory_path}: {e}")
        return None


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: Entry not found - {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        sys.exit(1)


def check_duplicate_urls_in_latest_entry():
    list_of_files = list_files(APP_CHAIN_DIRECTORY)
    data = download_json_file(JSON_URL)
    new_entry_loc = ""
    new_entry = None
    print(f"entries -> {list_of_files}")
    if list_of_files is not None:
        RPC_URLS = []
        METRICS_URLS = []
        EXPLORER_URLS = []
        IDS = []
        for entry in data:
            RPC_URLS.append(entry["rpc_url"])
            METRICS_URLS.append(entry["metrics_endpoint"])
            EXPLORER_URLS.append(entry["explorer_url"])
            IDS.append(entry["id"])
            
        for file in list_of_files:
            app_chain_id = file.split('.')[0]
            if app_chain_id not in IDS:
                new_entry_loc = APP_CHAIN_DIRECTORY + "/" + file
                
        if new_entry_loc == "":
            print("Error: entry already exists or invalid")
                sys.exit(1)

        new_entry = read_json_file(new_entry_loc)
        if not new_entry:
            print("Error: Latest entry does not")
            sys.exit(1)
        if new_entry and new_entry["rpc_url"] in RPC_URLS:
            print(f"Error: The RPC URL {new_entry['rpc_url']} is already present in the JSON file.")
            sys.exit(1)
        if new_entry and new_entry["metrics_endpoint"] in METRICS_URLS:
            print(
                f"Error: The metrics_endpoint  {new_entry['metrics_endpoint']} is already present in the JSON file.")
            sys.exit(1)
        if new_entry and new_entry["explorer_url"] in EXPLORER_URLS:
            print(f"Error: The Explorer URL {new_entry['explorer_url']} is already present in the JSON file.")
            sys.exit(1)
    print(f"duplicate check passed")
    return new_entry

        
def append_to_json_file(data, file_path):
    try:
        with open(file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        print(f"Data appended successfully to {file_path}")
    except Exception as e:
        print(f"Error in appending to file: {e}")
        sys.exit(1)

        
if __name__ == "__main__":
    latest_entry = check_duplicate_urls_in_latest_entry()
    if latest_entry:
        check_required_keys(latest_entry)
        check_url_status_code(latest_entry)
        append_to_json_file(latest_entry, LISTING_JSON_LOC)
