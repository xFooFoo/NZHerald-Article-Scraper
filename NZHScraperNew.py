import requests
import re
from bs4 import BeautifulSoup


url = input('What\'s the URL for the NZ Herald Article? ')
#url = 'https://www.nzherald.co.nz/business/we-didnt-have-any-food-in-the-house-asb-ceo-vittoria-shortt-on-her-tough-childhood-money-talks/TNURNHWFOBATTMFZF6EPR3ZSCM/#:~:text=ASB%20bank%20chief%20executive%20Vittoria,bank%20chief%20executive%20Vittoria%20Shortt.'
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


