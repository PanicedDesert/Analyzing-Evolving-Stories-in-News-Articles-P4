import os
import json
import xml.etree.ElementTree as ET

def xml_to_json(xml_file_path):
    # Parse XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Initialize dictionary to hold XML data
    xml_dict = {}
    
    # Initialize fullText variable
    fullText = []
    
    # Helper function for recursion
    def parse_element(element, parent_dict):
        nonlocal fullText
        tag = element.tag.split("}")[-1]  # Remove namespace
        text = element.text.strip() if element.text else ""
        
        new_entry = {}
        
        # Special handling for 'pubdata' tag
        if tag == 'pubdata':
            new_entry['attributes'] = element.attrib

        # Special handling for 'media-metadata' tag
        elif tag == 'media-metadata':
            attribute_name = element.attrib.get('name', '')
            attribute_value = element.attrib.get('value', '')
            new_entry = {attribute_name: attribute_value}
            
        elif element.attrib:
            if 'name' in element.attrib:
                attribute_name = element.attrib['name']
                new_entry = {attribute_name: element.attrib.get('content', "")}
            else:
                new_entry['attributes'] = element.attrib
                    
        if text:
            new_entry['text'] = text
        
        for child in element:
            parse_element(child, new_entry)
            
        if tag == 'p':
            if tag not in parent_dict:
                parent_dict[tag] = []
            parent_dict[tag].append(new_entry)
            if text:
                fullText.append(text)
        
        elif tag == 'media':  # Special handling for 'media' tag
            if tag not in parent_dict:
                parent_dict[tag] = []
            parent_dict[tag].append(new_entry)

        elif 'name' in element.attrib or tag == 'media-metadata':  # Handle 'name' and 'media-metadata' tags
            if tag not in parent_dict:
                parent_dict[tag] = {}
            parent_dict[tag].update(new_entry)
        else:
            parent_dict[tag] = new_entry



    
    # Start parsing from the root
    parse_element(root, xml_dict)
    
    # Add fullText to the xml_dict under the key 'fullText'
    xml_dict['fullText'] = ' '.join(fullText)
    
    # Convert dictionary to JSON string
    json_data = json.dumps(xml_dict, indent=4, ensure_ascii=False)
    
    return json_data

def process_folder(src_folder, dest_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    # Loop through all files and subfolders in the folder
    for entry in os.listdir(src_folder):
        entry_path = os.path.join(src_folder, entry)
        
        # If it's a folder, recursively process it
        if os.path.isdir(entry_path):
            new_dest_folder = os.path.join(dest_folder, entry)
            process_folder(entry_path, new_dest_folder)
        
        # If it's an XML file, convert it to JSON
        elif entry.endswith('.xml'):
            json_file_path = os.path.join(dest_folder, f"{os.path.splitext(entry)[0]}.json")
            
            # Convert XML to JSON
            json_data = xml_to_json(entry_path)
            
            # Write JSON data to file
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)

# Starting folder paths
xml_start_folder = 'files'
json_start_folder = 'converted'

# Start processing from the root folder
process_folder(xml_start_folder, json_start_folder)
