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

        return jsonify({"fetchStatus": f"Error when fetching article from {url}:\n {str(e)} 💀💀💀"}), 500

def is_wanted_element(elem):
    # Onlt include images with a source
    if elem.name == 'img':
        return 'src' in elem.attrs
    # Remove social link buttons/list items
    if elem.name == 'li' and elem.find('button', attrs={'data-test-ui': lambda x: x and 'social-link' in x}):
        return False
    # Viva premium articles with data-test-ui="article__action-bar" has this
    if elem.name == 'p' and 'Share this article:' in elem.text:
        return False
    return True  # Keep p or other li

def returnTagText(article_sections):
    content = []
    for article_section in article_sections:
        if article_section:
            article_elements = list(filter(is_wanted_element, article_section.find_all(['p', 'li', 'img'])))
            for elem in article_elements:
                if elem.name == 'p' or elem.name == 'li':
                    content.append({'type': 'text', 'content': elem.text})
                elif elem.name == 'img':
                    caption = None
                    alt = elem.get('alt', "Image goes here")
                    figure = elem.find_parent('figure')
                    if figure:
                        figcaption = figure.find('figcaption')
                        if figcaption:
                            caption = figcaption.text.strip()
                    content.append({'type': 'image', 'src': elem.get("data-src") or elem['src'], 'srcset': elem.get("data-srcset") or elem.get("srcset"), 'alt': alt, 'caption': caption})
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
        else:
            viva_heading = soup.select_one('h1[data-test-ui="viva-article__heading"]')
            if viva_heading:
                title = viva_heading.text
            

        # Main sections containing actual article content we want to scrape
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