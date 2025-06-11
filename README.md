This script scrapes any NZ Herald article and outputs the content to a text file. 
Directly use my webapp hosted on: https://nzherald.vercel.app/

# Instructions
- ```pip install beautifulsoup4```
- ```pip install requests ```
- ```pip install docx```
- For the backend, all the dependencies are in requirements.txt
- Clone the repository

## Running the backend server
- ```cd NZHerald Article Scraper\backend```
- ```python app.py```

## Running the front end locally
- ```cd NZHerald Article Scraper\frontend```
- ```npm run start```
- Enter the NZH article URL
- Article content is displayed to the screen

## Running the python scraper script locally to download a txt or .docx file
- Open CMD & set directory to the file that has "NZHScraperNew.py"
- ```python NZHScraperNew.py```
- Enter the NZH article URL
- The article is now downloaded to the same location as the script (path displayed in terminal)

### Technologies used:
- Python 3.8.3
- Flask (Handles server routing and request-response logic. send_from_directory is used to serve the React Build)
- React (front end)
- Beautiful Soup 4 (Webscraping Library)
- python-docx (to write DOCX content)
- requests (to send HTTP requests)
- Vercel (to deploy and host my Flask app)
