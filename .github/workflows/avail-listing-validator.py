import json
import uuid

import requests
import sys

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


def check_duplicate_urls_in_latest_entry(main_json, latest_entry):
    RPC_URLS = []
    METRICS_URLS = []
    EXPLORER_URLS = []
    IDS = []
    for entry in main_json:
        RPC_URLS.append(entry["rpc_url"])
        METRICS_URLS.append(entry["metrics_endpoint"])
        EXPLORER_URLS.append(entry["explorer_url"])
        IDS.append(entry["id"])

    if latest_entry["rpc_url"] in RPC_URLS:
        print(f"Error: The RPC URL {latest_entry['rpc_url']} is already present in the JSON file.")
        sys.exit(1)
    if latest_entry["metrics_endpoint"] in METRICS_URLS:
        print(f"Error: The metrics_endpoint  {latest_entry['metrics_endpoint']} is already present in the JSON file.")
        sys.exit(1)
    if latest_entry["explorer_url"] in EXPLORER_URLS:
        print(f"Error: The Explorer URL {latest_entry['explorer_url']} is already present in the JSON file.")
        sys.exit(1)
    if latest_entry["id"] in IDS:
        print(f"Error: The ID {latest_entry['id']} is already present in the JSON file.")
        sys.exit(1)


if __name__ == '__main__':
    new_entry = validate_json_array(sys.argv[1])
    data = download_json_file(JSON_URL)
    if new_entry and len(new_entry) > 0 and data != new_entry:
        latest_entry = new_entry[0]
        check_required_keys(obj=latest_entry)
        check_url_status_code(obj=latest_entry)
        check_duplicate_urls_in_latest_entry(data, latest_entry)
