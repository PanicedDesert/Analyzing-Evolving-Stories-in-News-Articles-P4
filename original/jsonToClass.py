import json
import os
import csv

class Article:
    next_id = 1

    def __init__(self, json_file):
        if os.path.getsize(json_file) == 0:
            # If it's an empty file, set default values
            self.ID = 0
            self.date_release = ''
            self.zone = ''
            self.author = ''
            self.headline = ''
            self.byline = ''
            self.paragraph = ''
            self.actual_article = False
            self.length_array = {
                "headline": 0,
                "byline": 0,
                "paragraph": 0
            }
            self.filename = os.path.basename(json_file)
            self.headline_stripped = ''
            self.byline_stripped = ''
            self.paragraph_stripped = ''
        else:
            with open(json_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # Handle JSON decoding error (e.g., invalid JSON)
                    # Set default values for this article
                    data = {}
            
            

            if 'nitf' in data:
                self.ID = Article.next_id
                Article.next_id += 1

                nitf_data = data['nitf']
                if 'head' in nitf_data and 'meta' in nitf_data['head'] and 'SAXo-Zone' in nitf_data['head']['meta']:
                    self.zone = nitf_data['head']['meta']['SAXo-ZoneShort']
                else:
                    self.zone = ''
                if 'head' in nitf_data and 'meta' in nitf_data['head'] and 'SAXo-Author' in nitf_data['head']['meta']:
                    self.author = nitf_data['head']['meta']['SAXo-Author']
                else:
                    self.author = ''
                if 'head' in nitf_data and 'docdata' in nitf_data['head']:
                    self.date_release = nitf_data['head']['docdata']['date.release']['attributes']['norm'].split('T')[0]
                else:
                    self.date_release = ''
            else:
                self.date_release = ''
                self.zone = ''
                self.author = ''
                self.ID = -1

            if 'body' in data.get('nitf', {}):
                body_data = data['nitf']['body']
                if 'body.head' in body_data and 'hedline' in body_data['body.head']:
                    hedline_data = body_data['body.head']['hedline']
                    hl1_text = hedline_data.get('hl1', {}).get('text', '').replace('\n', ' ')
                    hl2_text = hedline_data.get('hl2', {}).get('text', '').replace('\n', ' ')
                    if hl1_text and hl2_text:
                        self.headline = f"{hl1_text} {hl2_text}"
                    elif hl1_text:
                        self.headline = hl1_text
                    elif hl2_text:
                        self.headline = hl2_text
                    else:
                        self.headline = ''
                else:
                    self.headline = ''

                if 'byline' in body_data.get('body.head', {}):
                    if 'text' in body_data['body.head'].get('byline', {}):
                        self.byline = body_data['body.head']['byline']['text'].replace('\n', ' ')
                    else:
                        self.byline = ''
                else:
                    self.byline = ''

                self.paragraph = data['fullText']

            else:
                self.headline = ''
                self.byline = ''
                self.paragraph = ''

            self.actual_article = False
            self.length_array = {
                "headline": len(self.headline),
                "byline": len(self.byline),
                "paragraph": len(self.paragraph)
            }
            self.filename = os.path.basename(json_file)
            self.headline_stripped = self.headline.lower().replace('\n', ' ')
            self.byline_stripped = self.byline.lower().replace('\n', ' ')
            self.paragraph_stripped = self.paragraph.lower().replace('\n', ' ')

# Root folder
root_folder = 'problem/2017-06-14/'

json_files = []
for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

# CSV file
csv_file = 'articles.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(["ID", "Date Release", "Zone", "Author", "Actual Article", "Filename", "Headline", "Byline", "Paragraph", "Headline Stripped", "Byline Stripped", "Paragraph Stripped", "Headline Length", "Byline Length", "Paragraph Length"])
    
    # Create instances
    articles = [Article(json_file) for json_file in json_files]
    
    # Write each article as a row in the CSV
    for article in articles:
        writer.writerow([article.ID, article.date_release, article.zone, article.author, article.actual_article, article.filename, article.headline, article.byline, article.paragraph, article.headline_stripped, article.byline_stripped, article.paragraph_stripped, article.length_array["headline"], article.length_array["byline"], article.length_array["paragraph"]])