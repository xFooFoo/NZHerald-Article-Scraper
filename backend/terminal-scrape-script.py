import requests
import re
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.parse

def extract_content(element, content):
    element_type = element.get("type")

    # Normal paragraphs
    if element_type == "text":
        content.append({
            "type": "text",
            "content": element.get("content", "")
        })

    # Headers
    elif element_type == "header":
        if element.get("content"):
            content.append({
                "type": "header",
                "content": element["content"]
            })

    # Images
    elif element_type == "image":
        image = element.get("image", element)

        if image.get("url"):
            content.append({
                "type": "image",
                "url": image["url"],
                "caption": image.get("caption")
            })

    # Raw HTML blocks
    elif element_type == "raw_html":
        soup = BeautifulSoup(element.get("content", ""), "html.parser")

        for tag in soup.find_all(["div", "li", "p"]):
            text = tag.get_text(" ", strip=True)

            if text:
                content.append({
                    "type": "text",
                    "content": text
                })

    # Nested elements
    if "items" in element:
        for item in element["items"]:
            extract_content(item, content)



# URL VALIDATION
url = "https://www.nzherald.co.nz/nz/politics/labour-candidate-backs-out-of-south-island-electorate-race-party-forced-to-reselect/2XP37KX6MFD4PDM2MFYLR36TTI/"


# Make request to fetch the URL        
headers = {
    "User-Agent": "Mozilla/5.0"
}
html = requests.get(url, headers=headers).text

match = re.search(
    r'Fusion\.globalContent=(\{.*?\});Fusion\.',
    html,
    re.DOTALL
)

if not match:
    print("Fusion.globalContent not found")
    exit()

data = json.loads(match.group(1))




elements_content = []
guestAuthorRole_content = []
credits_content = []

# print(data.keys())
# print(data["credits"])

for element in data["elements"]:
    extract_content(element, elements_content)

# for element in data["credits"]:
#     extract_content(element, credits_content)

for item in elements_content:
    if item["type"] == "text":
        print(item["content"])

    elif item["type"] == "image":
        print("[IMAGE]", item["url"])