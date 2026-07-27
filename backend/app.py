import requests
import re
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.parse

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://nzherald.vercel.app"]}})

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in [
        'http://localhost:3000',
        'https://nzherald.vercel.app',
    ]:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def serve_index():
    return render_template('index.html'), 200 # React Entry point


@app.route('/submit', methods=['POST'])
def scrape_data():
    try:
        payload = request.get_json(silent=True) or {}
        url = (payload.get('url') or '').strip()

        if not url:
            return jsonify({
                "fetchStatus": "Please enter an NZ Herald article URL 🙏",
                "content": [],
                "author": [],
                "title": ""
            }), 400

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed = urllib.parse.urlparse(url)
        if parsed.netloc not in ['www.nzherald.co.nz', 'nzherald.co.nz']:
            return jsonify({
                "fetchStatus": "Please enter a valid NZ Herald Article URL 🙏",
                "content": [],
                "author": [],
                "title": ""
            }), 400

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        html = requests.get(url, headers=headers, timeout=20).text

        match = re.search(
            r'Fusion\.globalContent=(\{.*?\});Fusion\.',
            html,
            re.DOTALL
        )

        if not match:
            return jsonify({
                "fetchStatus": "Could not find article content on that page 🙏",
                "content": [],
                "author": [],
                "title": ""
            }), 404

        article_data = json.loads(match.group(1))

        content = []
        for element in article_data.get("elements", []):
            extract_content(element, content)

        title = (
            article_data.get("title")
            or article_data.get("meta", {}).get("title")
            or article_data.get("headline")
            or "NZ Herald Article"
        )

        author = []
        raw_author = article_data.get("author") or article_data.get("authors") or []
        if isinstance(raw_author, dict):
            raw_author = [raw_author]

        if isinstance(raw_author, list):
            for person in raw_author:
                if isinstance(person, dict):
                    name = person.get("name") or person.get("title")
                    if name:
                        author.append({
                            "type": "text",
                            "subtype": None,
                            "content": name
                        })

        return jsonify({
            "fetchStatus": f"Fetched: {title}",
            "content": content,
            "author": author,
            "title": title
        })
    except requests.RequestException as e:
        return jsonify({
            "fetchStatus": f"Error when fetching article from {url}:\n {str(e)} 💀💀💀",
            "content": [],
            "author": [],
            "title": ""
        }), 500
    except Exception as e:
        return jsonify({
            "fetchStatus": f"Error when parsing article from {url}:\n {str(e)} 💀💀💀",
            "content": [],
            "author": [],
            "title": ""
        }), 500


def extract_content(element, content):
    if not isinstance(element, dict):
        return

    element_type = element.get("type")

    if element_type == "text":
        text = element.get("content", "")
        if text:
            content.append({
                "type": "text",
                "subtype": None,
                "content": text
            })

    elif element_type == "header":
        text = element.get("content", "")
        if text:
            content.append({
                "type": "text",
                "subtype": "header",
                "content": text
            })

    elif element_type == "image":
        image = element.get("image", element)
        image_url = image.get("url") or image.get("src")
        if image_url:
            content.append({
                "type": "image",
                "subtype": None,
                "src": image_url,
                "srcset": image.get("srcset") or None,
                "alt": image.get("alt") or "",
                "caption": image.get("caption") or None
            })

    elif element_type == "raw_html":
        soup = BeautifulSoup(element.get("content", ""), "html.parser")
        for tag in soup.find_all(["div", "li", "p"]):
            text = tag.get_text(" ", strip=True)
            if text:
                content.append({
                    "type": "text",
                    "subtype": None,
                    "content": text
                })

    if "items" in element and isinstance(element["items"], list):
        for item in element["items"]:
            extract_content(item, content)


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run()