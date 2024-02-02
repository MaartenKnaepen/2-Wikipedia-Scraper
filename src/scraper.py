import requests
from bs4 import BeautifulSoup
import re
from json import dumps
import json
import csv

class WikipediaScraper:
    """
    A class for scraping and retrieving information about country leaders from Wikipedia.

    Attributes:
    - base_url: The base URL for the Wikipedia scraper.
    - country_endpoint: The endpoint for obtaining information about available countries.
    - leaders_endpoint: The endpoint for retrieving information about country leaders.
    - cookies_endpoint: The endpoint for obtaining and refreshing cookies.
    - leaders_data: A dictionary to store leaders' information.
    - cookie: Cookies used for making requests to the scraper.
    - df: Pandas DataFrame to store the leader information.
    - leader_json: JSON representation of leader data.
    """

    def __init__(self):
        """
        Initialize the WikipediaScraper object.
        """
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = self.base_url + '/countries'
        self.leaders_endpoint = self.base_url + '/leaders'
        self.cookies_endpoint = self.base_url + '/cookie'
        self.cookie = requests.get(self.cookies_endpoint).cookies
        self.df = None
        self.leader_json = None

    def refresh_cookie(self):
        """
        Refresh the cookie used for making requests to the scraper.
        """
        self.cookie = requests.get(self.cookies_endpoint).cookies
        print('New cookie created!')

    def get_countries(self):
        """
        Retrieve and return information about available countries.

        Returns:
        - str: A string containing information about available countries.
        """
        self.countries = requests.get(self.country_endpoint, cookies=self.cookie)
        if self.countries.status_code != 200:
            self.refresh_cookie()
        self.countries = requests.get(self.country_endpoint, cookies=self.cookie)

        return self.countries.text

    def get_leaders(self) -> None:
        """
        Retrieve information about leaders of specific countries and store it in the leaders_data dictionary.
        """
        clist = ["ma", "us", "fr", "be", "ru"]
        self.leaders_data = []

        for c in clist:
            self.leader_country_endpoint = self.leaders_endpoint + '?country=' + c
            self.leader = requests.get(self.leader_country_endpoint, cookies=self.cookie)
            if self.leader.status_code != 200:
                self.refresh_cookie()
            self.dict_lst = ['id', 'first_name', 'last_name', 'birth_date', 'death_date', 'place_of_birth',
                             'wikipedia_url', 'start_mandate', 'end_mandate']
            self.leader_cntry = self.leader.json()

            # Initialize an empty dictionary for each country
            leaders_data_cntry = {}

            for a in self.dict_lst:
                # Check if key 'a' exists in the dictionary before accessing it
                if self.leader_cntry and all(a in leader for leader in self.leader_cntry):
                    leaders_data_cntry[a] = [leader[a] for leader in self.leader_cntry]
                else:
                    leaders_data_cntry[a] = []

            self.leaders_data.append(leaders_data_cntry)

        for country_data in self.leaders_data:
            for url in country_data['wikipedia_url']:
                country_data['biography'] = self.get_first_paragraph(url)

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        """
        Retrieve the first paragraph of a Wikipedia page given its URL.

        Args:
        - wikipedia_url (str): The URL of the Wikipedia page.

        Returns:
        - str: The first paragraph of the Wikipedia page.
        """
        self.wikipedia_url = wikipedia_url
        self.r = requests.get(wikipedia_url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')

        for self.elem in self.soup.find_all('p'):
            if self.elem.find('b'):
                self.paragraph = self.elem.text
                break

        regex_pattern = r'\[[^\]]*\]|\([^\)]*\)|[^\w\s,.\'-]'
        self.paragraph = re.sub(regex_pattern, "", self.paragraph)    # Remove all brackets and text between brackets
        self.paragraph = re.sub(r'\s{2,}', " ", self.paragraph)       # Reduce all multiple spaces to one space
        self.paragraph = re.sub(r'\s+([.,])', r'\1', self.paragraph)    # Remove spaces before points or commas
        return self.paragraph

    def save_data(self, filetype, filename):
        """
        Save the scraped data to the specified file type.

        Args:
        - filetype (str): The type of file to save (json, excel, or csv).
        - filename (str): The name of the file to save the data.

        Raises:
        - ValueError: If an invalid filetype is provided.
        """
        self.filetype = filetype
        self.filename = filename
        if self.filetype == "excel":
            self.df.to_excel(self.filename)
        elif self.filetype == "json":
            #self.to_json()
            with open(f'{self.filename}.json', "w", encoding="utf-8") as file:
                json.dump(self.leaders_data, file, indent=4)
                
        
    def to_json(self):
        """
        Convert the scraped data to JSON format.
        """
        self.dumps = json.dump(self.leaders_data, indent=2)

    def __repr__(self) -> str:
        return "This is a WikipediaScraper object."
