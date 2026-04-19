Scrape any NZHerald article using --> https://nzherald.vercel.app/

# Instructions
- ```pip install beautifulsoup4```
- ```pip install requests ```
- ```pip install docx```
- Clone the repository

## Running the backend server
- ```cd NZHerald Article Scraper\backend```
- ```pip install -r requirements.txt```
- ```python app.py```

## Running the front end locally
- ```cd NZHerald Article Scraper\frontend```
- Compile the code: ```npm run build```
- ```npm install -g serve```
- Run the app on localhost port 3000: ```serve -s build -l 3000```
- Enter the NZH article URL
- Article content is displayed to the screen

## Running the python scraper script locally to download a txt or .docx file
- Open CMD & set directory to the file that has "NZHScraperNew.py"
- ```python NZHScraperNew.py```
- Enter the NZH article URL
- The article is now downloaded to the same location as the script (path displayed in terminal)

## Production Deployment to Vercel
- To update your Production Deployment automatically, push to the main branch.
- Any feature branch is deployed to a preview...
- Deploy ```/backend``` folder to [nzherald](https://vercel.com/xfoofoos-projects/nzherald)
- Deploy ```/frontend``` folder to [nzherald-server](https://vercel.com/xfoofoos-projects/nzherald-server)

### Technologies used:
- Python 3.8.3
- Flask (Handles server routing and request-response logic. send_from_directory is used to serve the React Build)
- React (front end)
- serve (host frontend locally)
- Beautiful Soup 4 (Webscraping Library)
- python-docx (to write DOCX content)
- requests (to send HTTP requests)
- Vercel (to deploy and host my Flask app)
