from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import urllib.parse

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
        
        # Normalize the URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Check domain/host of the URL
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc not in ['www.nzherald.co.nz', 'nzherald.co.nz']:
            return jsonify({"fetchStatus": "Please enter a valid NZ Herald Article URL 🙏"}), 400

        title, author, content = scrapeContent(url)
        
        if not content:
            return jsonify({"fetchStatus": "No content found in the article 😞"}), 204
        
        print(f"Received value: {url}")
        
        # Respond with a success message
        return jsonify({
            "fetchStatus": "Article scraped successfully! 😁",
            "title": title,
            "content": content
        }), 200
    except Exception as e:

        return jsonify({"fetchStatus": f"Error when fetching article from {url}:\n {str(e)} 💀💀💀"}), 500

# Filtering only wanted HTML elements
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

# Serializing <p>/<li> tags' content into text to be rendered as HTML in frontend
def serialize_paragraph(elem: Tag):
    parts = []
    for child in elem.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif child.name == 'a':
            href = child.get('href')
            text = child.string or child.get_text(strip=True)
            if href:
                parts.append(f'<a href="{href}" target="_blank" rel="noreferrer">{text}</a>')
            else:
                parts.append(text)
        else:
            parts.append(child.get_text())
    return ''.join(parts)

# Handles retrieving the text for all kinds of HTML tags
def returnTagText(article_sections):
    content = []
    for article_section in article_sections:
        if article_section:
            article_elements = list(filter(is_wanted_element, article_section.find_all(['p', 'li', 'img'])))
            for elem in article_elements:
                if elem.name == 'p' or elem.name == 'li':
                    content.append(returnElementTextContent(elem))
                elif elem.name == 'img':
                    content.append(returnImageContent(elem))
    return content

def returnElementTextContent(elem):
    return {'type': 'text', 'content': elem.decode_contents()}

def returnImageContent(elem):
    caption = None
    alt = elem.get('alt', "Image goes here")
    figure = elem.find_parent('figure')
    if figure:
        figcaption = figure.find('figcaption')
        if figcaption:
            caption = figcaption.text.strip()
    return {'type': 'image', 'src': elem.get("data-src") or elem['src'], 'srcset': elem.get("data-srcset") or elem.get("srcset"), 'alt': alt, 'caption': caption}
                    
def scrapeTitle(soup):
    title_section = soup.select_one('h1[data-test-ui="article__heading"]')
    if title_section:
        return title_section.text
    else:
        viva_heading = soup.select_one('h1[data-test-ui="viva-article__heading"]')
        if viva_heading:
            return viva_heading.text

def scrapeAuthor(soup):
    content = []
    
    author_img = soup.select_one('img[data-test-ui="author--details__image"]')
    author_role = soup.select_one('span[data-test-ui="author--role"]')
    author_distributor_name = soup.select_one('span[data-test-ui="distributor--name"]')
    author_display_date = soup.select_one('time[data-test-ui="author-display--date"]')
    author_read_time = soup.select_one('span[data-test-ui="author-read-time"]')
    
    author_elements = [author_role, author_distributor_name, author_display_date, author_read_time]
    
    content.append(returnImageContent(author_img))
    for elem in author_elements:
        content.append(returnElementTextContent(elem))
        
    return content

# Determines which sections of the article to scrape
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
        title = scrapeTitle(soup)
        
        # Author Portion
        author = scrapeAuthor(soup)
        
        # Main sections containing actual article content we want to scrape
        article_sections = [soup.select_one('section[data-test-ui="article__body"]'),
                            soup.select_one('section[data-test-ui="article-top-body"]'),
                            soup.select_one('section[data-test-ui="article-bottom-body"]')]
        content = returnTagText(article_sections)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
    return title, author, content

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run()