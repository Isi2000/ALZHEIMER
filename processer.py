import os
import json
from tqdm import tqdm

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        result = {}  # Create an empty dictionary to store the results
        for item in data:
            if 'Id' in item and 'cited_arts' in item:
                result[item['Id']] = item['cited_arts']
        return result  # Return the dictionary

def process_directory(directory_path):
    results = {}  # Create an empty dictionary to accumulate results
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                result = process_json_file(file_path)
                results.update(result)  # Update the results dictionary
    return results  # Return the final dictionary

# Replace 'path_to_directory' with the actual path of your directory containing the JSON files.
path_to_directory = './DATA'
results = process_directory(path_to_directory)
print(results)
