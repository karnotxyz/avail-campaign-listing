import json
import uuid
import os
import requests
import sys

APP_CHAIN_DIRECTORY = os.path.join(os.getcwd(), "app_chains")
JSON_URL = "https://api.github.com/repos/karnotxyz/avail-campaign-listing/contents/app_chains"
TIMEOUT_IN_MS = 500


def validate_json_array(json_file):
    with open(json_file, 'r') as file:
        listing = json.load(file)

    if not isinstance(listing, list):
        print(f"Error: The JSON file {json_file} does not contain a JSON array.")
        sys.exit(1)
    return listing


def download_json_file(url):
    response = requests.get(url, timeout=TIMEOUT_IN_MS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Failed to download JSON file from {url}.")


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
        IDS = []
        RPC_URLS = []
        METRICS_URLS = []
        EXPLORER_URLS = []
        new_entry_app_chain_id = None
        for entry in data:
            IDS.append(entry["name"].split('.')[0])

        for file in list_of_files:
            temp_file = None
            app_chain_id = file.split('.')[0]
            if app_chain_id not in IDS:
                # check .json exists in filename at the end and is present only once
                if not (file.endswith(".json") and file.count(".json") == 1):
                    print(f"Error: The file {file} is not a valid JSON file.")
                    sys.exit(1)
                new_entry_loc = APP_CHAIN_DIRECTORY + "/" + file
                new_entry_app_chain_id = file.split('.')[0]
            else:
                temp_file = read_json_file(APP_CHAIN_DIRECTORY + "/" + file)
                RPC_URLS.append(temp_file.get('rpc_url'))
                METRICS_URLS.append(temp_file.get("metrics_endpoint"))
                EXPLORER_URLS.append(temp_file.get("explorer_url"))

        if new_entry_loc == "":
            print("Error: entry already exists or invalid")
            sys.exit(1)

        new_entry = read_json_file(new_entry_loc)
        if not new_entry:
            print("Error: Latest entry does not")
            sys.exit(1)
        if new_entry_app_chain_id and new_entry_app_chain_id != new_entry["id"]:
            print(f"Error: File Name & App Chain Id is not same. ID-> {new_entry['id']}, FileName -> {new_entry_app_chain_id}.")
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


if __name__ == "__main__":
    latest_entry = check_duplicate_urls_in_latest_entry()
    if latest_entry:
        check_required_keys(latest_entry)
        check_url_status_code(latest_entry)
