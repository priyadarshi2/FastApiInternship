import json
import os

def load_json():
    # Check if the file exists before trying to read it
    if not os.path.exists('opinions.json'):
        # Create an empty JSON file if it does not exist
        with open('opinions.json', 'w') as file:
            json.dump({}, file)
    
    # Read dictionary from JSON file
    with open('opinions.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(data: dict):
    with open('opinions.json', 'w') as file:
        json.dump(data, file, indent=4)

def update_json(new_data: dict): 
    data = load_json() 
    data.update(new_data) 
    write_json(data) 

def append_json(new_data : dict):
    update_json(new_data)

def extract_value(key: str):
    data = load_json()
    return data[key]

def search_key(key: str):
    data = load_json()
    if key in data:
        return True
    else:
        return False

