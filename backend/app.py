from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app) 

@app.route('/')
def serve_index():
    return render_template('index.html'), 200 # React Entry point

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