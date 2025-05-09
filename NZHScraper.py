import requests
from bs4 import BeautifulSoup

url = 'https://www.nzherald.co.nz/nz/politics/golriz-ghahraman-case-experts-explain-complex-ptsd-and-loss-reactive-shoplifting/4CZZOYXJTVAZPMIRXFBGJ5X3VA/'
response = requests.get(url)
content = ""

# Check if the request was successful
if response.status_code == 200:
    

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Title Portion
    title = soup.find(class_='article__heading').text
    content += "Title: " + title + "\n\n"

    # Body Text Portion
    parent_section = soup.select_one('section[data-test-ui="article__body"][data-ref-group="body"]')
    if parent_section:
        paragraphs = parent_section.find_all('p')
        # Extract and print the text content of each element
        for paragraph in paragraphs:
            content += paragraph.text + "\n\n"

    # Write content to a txt file
    #file_path = title + ".txt"
    file_path = "abc.txt"
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        # Write the content to the file
        file.write(content)
    print(f"Content written to \"{file_path}\"")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


