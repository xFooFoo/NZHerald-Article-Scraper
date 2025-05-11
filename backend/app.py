from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from docx import Document
from bs4 import BeautifulSoup
import requests
import re
import os

static_dir = os.path.join(os.path.dirname(__file__), './frontend/build')
app = Flask(__name__, static_folder=static_dir, static_url_path='')
CORS(app) 

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html'), 200 # React Entry point

# This serves JS, CSS, manifest, etc.
@app.route('/<path:path>')
def serve_static_file(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/submit', methods=['POST'])
def scrape_data():
    try:
        data = request.get_json()  # Get the JSON data from the request body
        url = data.get('url')  # Access the value sent from React
        title, content = scrapeContent(url)

        # You can now process the data (e.g., store in a database, etc.)
        print(f"Received value: {url}")
        
        # Respond with a success message
        return jsonify({
            "fetchStatus": "Article scraped successfully!!! 😁😁😁",
            "title": title,
            "content": content
        }), 200
    except Exception as e:
        return jsonify({"fetchStatus": f"Error: Invalid URL {url} 💀💀💀"}), 500

# Required for Vercel
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

def scrapeContent(url):
    response = requests.get(url)
    content = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = str(soup.find(class_='article__heading').text)

        parent_section = soup.select_one('section[data-test-ui="article__body"]')
        if parent_section:
            paragraphs = parent_section.find_all('p')
            for paragraph in paragraphs:
                content.append(paragraph.text)

        parent_section = soup.select_one('section[data-test-ui="article-top-body"]')
        if parent_section:
            paragraphs = parent_section.find_all('p')
            for paragraph in paragraphs:
                content.append(paragraph.text)

        parent_section = soup.select_one('section[data-test-ui="article-bottom-body"]')
        if parent_section:
            paragraphs = parent_section.find_all('p')
            for paragraph in paragraphs:
                content.append(paragraph.text)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return title, content
# if __name__ == '__main__':
#     print("Starting Flask server...")
#     app.run()