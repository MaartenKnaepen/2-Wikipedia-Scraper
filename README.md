# Wikipedia Scraper
Wikipedia Scraper is a Python program designed for efficiently scraping information about country leaders from Wikipedia. The tool offers a command-line interface, allowing users to interactively select countries, customize data options, and save the scraped information in various file formats.

## Installation
To install Wikipedia Scraper, follow these steps:

Clone the repository to your local machine using the command:
```
git clone https://github.com/your_username/LeaderScraper.git
```
cd LeaderScraper

Ensure that you have the required dependencies installed by executing:
```
pip install -r requirements.txt
```
## Features
LeaderScraper provides the following features:

### Country Selection: 
Users can choose countries of interest from a predefined list.
Biographical Information: An option to include short biographies for each country's leader.
File Format Options: Choose to save the scraped data in Excel, CSV, or JSON formats.
### How to Use
Run the main script using the command:
```
python main.py
```
Follow the on-screen prompts to:

Select countries by entering the corresponding numbers.
Indicate whether to include short biographies for leaders.
Choose the desired file format for saving the data.
Upon completion, the program will save the scraped data in the specified file format with the filename "leaders" (e.g., leaders.xlsx, leaders.json, leaders.csv).
