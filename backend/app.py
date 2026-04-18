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
        
        # Some url/content checks
        if not url.startswith("https://www.nzherald.co.nz/"):
            return jsonify({"fetchStatus": "Please enter a valid NZHerald Article URL 🙏🙏🙏"}), 400

        if not content:
            return jsonify({"fetchStatus": "No content found in the article. Please check the URL 🙏"}), 400
        
        print(f"Received value: {url}")
        
        # Respond with a success message
        return jsonify({
            "fetchStatus": "Article scraped successfully!!! 😁😁😁",
            "title": title,
            "content": content
        }), 200
    except Exception as e:
        print(f"Unexpected Exception {str(e)}")
        return jsonify({"fetchStatus": f"Error when fetching article from {url} 💀💀💀"}), 500

def scrapeContent(url):
    response = requests.get(url)
    content = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Title Portion
        heading = soup.select_one('h1[data-test-ui="article__heading"]')
        if heading:
            title = heading.text 
        else:
            title = "Title not found"

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
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run()