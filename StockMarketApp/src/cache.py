import json
import os

def load_json():
    # Read dictionary from JSON file
    if not os.path.exists('opinions.json'):
        with open('opinions.json', 'w') as file: 
            json.dump({}, file)
    with open('opinions.json', 'r') as file:
            return file

def write_json(data : dict):
    file = load_json()
    json.dump(data, file)

def extract_value(key : str): 
    file = load_json()
    data = json.load(file)
    return data[key]      
    
def search_key(key : str): 
    file = load_json()
    data = json.load(file)
    if key in data: 
        return True 
    else: 
        return False