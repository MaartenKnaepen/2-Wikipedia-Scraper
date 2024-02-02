# Wikipedia Scraper
Wikipedia Scraper is a Python program designed to scrape information about country leaders from the https://country-leaders.onrender.com api. Additionally, it scrapes Wikipedia to provide a short biography It utilizes the BeautifulSoup library for web scraping and provides an interface to interact with the data through different output formats such as JSON, Excel, and CSV.

## Table of Contents
Installation
Usage
Dependencies
Functionalities
Documentation

### Installation
Clone the repository:
```
git clone https://github.com/your-username/2-Wikipedia-Scraper.git
```

Install the required dependencies:
```
pip install -r requirements.txt
```
### Usage
To run the Wikipedia Scraper program, execute the main.py script:

```
python main.py
```
Follow the on-screen instructions to interact with the program and choose from available options. The following options are available:

Available Countries (Press 1):

Displays a list of available countries.

Leaders of All Countries (Press 2):

Initiates the scraping process to gather information about leaders of selected countries.
Saves the data in JSON format and provides information about the saved file.

Close the Program (Press 3):

Exits the LeaderScraper program.

Additionally, the program provides feedback for invalid inputs.

### Dependencies
Wikipedia Scraper relies on the following Python libraries:

requests
BeautifulSoup
json
Install these dependencies using the provided requirements.txt file:

```
pip install -r requirements.txt
```
### Functionalities
LeaderScraper provides the following functionalities:

Retrieve information about available countries.
Obtain details about leaders of specific countries.
Save the scraped data in a leaders.json file.
### Documentation
The WikipediaScraper class within scraper.py is the core component of LeaderScraper. 
For detailed documentation about the class and its methods, refer to the comments and docstrings in the scraper.py file.
