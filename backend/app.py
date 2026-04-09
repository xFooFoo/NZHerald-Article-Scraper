from flask import Flask, request, jsonify, render_template
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

        return jsonify({"fetchStatus": f"Error when fetching article from {url}:\n {str(e)} 💀💀💀"}), 500

def returnTagText(article_sections):
    content = []
    for article_section in article_sections:
        if article_section:
            article_lines = article_section.find_all(['p', 'li'])
            for line in article_lines:
                content.append(line.text)
    return content

def scrapeContent(url):
    title = "Title not found"
    content = []
    
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as err:
        print(f"Request failed: {err}")
        return title, content
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Title Portion
        heading = soup.select_one('h1[data-test-ui="article__heading"]')
        if heading:
            title = heading.text 

        article_sections = [soup.select_one('section[data-test-ui="article__body"]'),
                            soup.select_one('section[data-test-ui="article-top-body"]'),
                            soup.select_one('section[data-test-ui="article-bottom-body"]')]
        content = returnTagText(article_sections)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
    return title, content

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run()