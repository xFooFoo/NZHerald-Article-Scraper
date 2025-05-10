This script scrapes any NZ Herald article and outputs the content to a text file. 

# Instructions
- ``` pip install beautifulsoup4  ```
- ``` pip install requests ```
- ``` pip install docx```
- For the backend, all the depedencies are in requirements.txt
- Clone the repository
- Either run "NZHScraperNew.py" and enter the NZH article URL
	or
  Change the url variable in "NZHScraper.py" to any NZH articke and run
- Open CMD & set directory to the file that has "NZHScraperNew.py"
- ```python NZHScraperNew.py```

### Technologies used:
- Python 3.8.3
- Flask (Handles server routing and request-response logic. send_from_directory is used to serve the React Build)
- React (front end)
- Beautiful Soup 4 (Webscraping Library)
- python-docx (to write DOCX content)
- requests (to send HTTP requests)
