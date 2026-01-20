import os
import json
import numpy as np
import pandas as pd
import ownfunc
import json
import pprint as pprint

json_dataset = r"C:\Users\mikke\Desktop\nesws_json"

category_df = pd.DataFrame(
    columns=["Category", "Article_Count", "Sum_Total_For_Category"])


def add_or_update_row(df, category, sum_total_increment):
    if category in df["Category"].values:
        # Category exists, update the values
        index = df[df["Category"] == category].index[0]
        df.loc[index, "Article_Count"] += 1
        df.loc[index, "Sum_Total_For_Category"] += sum_total_increment
    else:
        # Category doesn't exist, add a new row with the increments
        df.loc[len(df)] = [category, 1,
                           sum_total_increment]

def _print_info(doc_list):
    total_length = 0
    length_count = 0
    count_with = 0
    count_none = 0

    for item in doc_list:
        if len(item) > 0:  # Ensure the item is not an empty string
            #print(item[:300])
            count_with += 1

        else:
            #print("-")
            count_none += 1
    for item in doc_list:
        if len(item) > 0:  # Ensure the item is not an empty string
            total_length += len(item)
            length_count += 1
    if length_count > 0:
        average_length = total_length / length_count
    else:
        average_length = 0  # Handle the case where the array is empty
    print("count: ", count_with)
    print("count_none: ", count_none)
    print("Average Length:", average_length)
    print("articler", count_with+count_none)

def append_docs(json_doc, text_field, doc_list, meta_tag, article_categories, find_popular_categories=True):
    if isinstance(json_doc, dict):
        #print(data.get("nitf", {}).get("head", {}).get("meta", {}).get(
        #    meta_type))
        if json_doc.get("nitf", {}).get("head", {}).get("meta", {}).get(meta_tag) in article_categories:
            for key, text in json_doc.items():
                if key == text_field:
                    #print("key: ", key)
                    meta_type_in_article = json_doc.get("Meta_type:", json_doc.get("nitf", {}).get(
                        "head", {}).get("meta", {}).get(meta_tag))
                    doc_list.append(text)
                    if find_popular_categories == True:
                        add_or_update_row(
                            category_df, meta_type_in_article, len(text))
                elif isinstance(text, (dict, list)):
                    append_docs(
                        text, text_field, doc_list, meta_tag, article_categories)
    elif isinstance(json_doc, list):
        for item in json_doc:
            append_docs(
                item, text_field, doc_list, meta_tag, article_categories)


text_field = "fullText"
meta_type = "SAXo-ZoneShort"
all_categories = ownfunc.find_themes_catogories(
    json_dataset)


doc_list = []


def get_text_doc(json_path, category_list, find_categories=True, find_docs=True, print_info=True):
    doc_list = []
    for root, dirs, files in os.walk(json_path):
        for filename in files:
            # Check if the file nhas a .json extension
            if filename.endswith('.json'):
                # Construct the full file path
                file_path = os.path.join(root, filename)
                try:
                    # Attempt to open and parse the JSON file
                    with open(file_path, 'r', encoding="utf-8") as json_doc:
                        json_doc = json.load(json_doc)
                    # If successful, you can process the JSON data here
                    #print(f'Found JSON file: {file_path}')
                    if find_docs == True:
                        append_docs(
                            json_doc, text_field, doc_list, meta_type, category_list, find_categories)
                    #print("counting")
                except json.JSONDecodeError as e:
                    # Handle the case where the file is not valid JSON
                    print(f'Error parsing JSON in file: {file_path}')
                except Exception as e:
                    # Handle other exceptions (e.g., file not found)
                    print(f'Error processing file: {file_path}, {str(e)}')
    if print_info:
        _print_info(doc_list)
    return doc_list
        


doc_list_for_categories = get_text_doc(json_dataset, all_categories)



category_df["Average_length"] = category_df["Sum_Total_For_Category"] / \
    category_df["Article_Count"]

pd.set_option('display.max_columns', 10)


sorted_data = category_df.sort_values(by='Average_length', ascending=False)

filtered_data = sorted_data[sorted_data['Article_Count'] > 50]
popular_categories = list(filtered_data["Category"].values)
popular_categorie_count = len(popular_categories)

#print(popular_categories)
#print("countings:", popular_categorie_count)



print("")
sorted_doc_list = get_text_doc(json_dataset,
             popular_categories, find_categories=False)

