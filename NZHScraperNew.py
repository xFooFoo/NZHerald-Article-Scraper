import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.nzherald.co.nz/nz/politics/health-transport-housing-major-announcements-to-come-in-final-days-of-christopher-luxons-action-plan/IA454F6OBZBIZMIEKHJARRGITM/'
response = requests.get(url)
content = ""

# Check if the request was successful
if response.status_code == 200:
    

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Title Portion
    title = str(soup.find(class_='article__heading').text)
    content += "Title: " + title + "\n\n"

    # Body Text Top Portion
    parent_section = soup.select_one('section[data-test-ui="article-top-body"]')
    if parent_section:
        paragraphs = parent_section.find_all('p')
        # Extract and print the text content of each element
        for paragraph in paragraphs:
            content += paragraph.text + "\n\n"

    # Body Text Bottom Portion
    parent_section = soup.select_one('section[data-test-ui="article-bottom-body"]')
    if parent_section:
        paragraphs = parent_section.find_all('p')
        # Extract and print the text content of each element
        for paragraph in paragraphs:
            content += paragraph.text + "\n\n"

    # Write content to a txt file
    # filename can't have these special chars
    file_path = re.sub("[\\\\/:*?\"<>|]", "", title) + ".txt"
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        # Write the content to the file
        file.write(content)
    print(f"Content written to \"{file_path}\"")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


