import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import joblib
import string
import json
import glob
import os



def stopword_reader():
    with open("Kode\stopord.txt", 'r',encoding="utf-8") as file:
        stopwords_danish = []
        # Iterate over each line in the file
        for line in file:
            # Process each line here (e.g., print it)
            line = line.replace("\n", "")
            stopwords_danish.append(line)
    return stopwords_danish


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)


def write_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def find_themes_catogories(path):
    def find_themes(json_doc, meta_tag, result_list):
        if isinstance(json_doc, dict):
            result_list.append(json_doc.get("nitf", {}).get("head", {}).get(
                "meta", {}).get(meta_tag))
        elif isinstance(json_doc, list):
            for item in json_doc:
                find_themes(
                    item, meta_tag, result_list)
    categories_list = []
    meta_tag = "SAXo-ZoneShort"
    counter_files = 0 
    for root, dirs, files in os.walk(path):
        for filename in files:
            # Check if the file nhas a .json extension
            if filename.endswith('.json'):
                counter_files +=1
                print("nr: ", counter_files, " :")
                # Construct the full file path
                file_path = os.path.join(root, filename)
                try:
                    # Attempt to open and parse the JSON file
                    with open(file_path, 'r', encoding="utf-8") as json_file:
                        json_doc = json.load(json_file)
                    # If successful, you can process the JSON data here
                    print(f'Category:Found JSON file: {file_path}')
                    find_themes(json_doc, meta_tag, categories_list)
                except json.JSONDecodeError as e:
                    # Handle the case where the file is not valid JSON
                    print(f'Category:Error parsing JSON in file: {file_path}')
                    continue
                except Exception as e:
                    # Handle other exceptions (e.g., file not found)
                    print(
                        f'Category:Error processing file: {file_path}, {str(e)}')
                    continue
    

    categories_list_uniques = list(set(categories_list))
    return categories_list_uniques