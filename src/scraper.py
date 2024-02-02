import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from json import loads
import json
import threading
import multiprocessing

class WikipediaScraper:
    """
    WikipediaScraper class for scraping information about country leaders from Wikipedia.

    Attributes:
    - base_url (str): The base URL for the Wikipedia scraper.
    - country_endpoint (str): The endpoint for obtaining information about available countries.
    - leaders_endpoint (str): The endpoint for retrieving information about country leaders.
    - cookies_endpoint (str): The endpoint for obtaining and refreshing cookies.
    - leaders_data (dict): Dictionary to store leader information.
    - cookie: Cookies used for making requests to the scraper.
    - df: Pandas DataFrame to store leader information.
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
        self.leaders_data = {}
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

    def get_leaders(self, country: str) -> None:
        """
        Retrieve information about leaders of a specific country.

        Args:
        - country (str): The code representing the country.

        Returns:
        - dict: JSON representation of leader data.
        """
        if country in ["ma", "us", "fr", "be", "ru"]:
            self.country = '?country=' + country
            self.leader_country_endpoint = self.leaders_endpoint + self.country

            with requests.Session() as session:
                self.leader = session.get(self.leader_country_endpoint, cookies=self.cookie)
                if self.leader.status_code != 200:
                    self.refresh_cookie()
                self.leader = session.get(self.leader_country_endpoint, cookies=self.cookie)
            self.leader_json = self.leader.json()
            return self.leader_json

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

    def append_wiki_bio(self, url, bio):
        """
        Append Wikipedia biography to the bio list if the URL is not None.

        Args:
        - url (str): The Wikipedia URL.
        - bio (list): The list to append biographies to.
        """
        if url is not None:
            paragraph = self.get_first_paragraph(url)
            bio.append(paragraph)

    def append_wiki_bio_multi(self):
        """
        Append Wikipedia biographies in parallel using multiple threads.
        """
        bio = []
        threads = []
        x = int(multiprocessing.cpu_count() * 0.8)
        sublists = [self.outputdf['wikipedia_url'][i:i + x] for i in range(0, len(self.outputdf['wikipedia_url']), x)]

        for sublist in sublists:
            # Create Threads for reading input
            for url in sublist:
                thread = threading.Thread(target=self.append_wiki_bio, args=(url, bio))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish before continuing
            for thread in threads:
                thread.join()

        self.outputdf['biography'] = bio

    def into_dataframe(self):
        """
        Convert leader_json data to Pandas DataFrame.
        """
        self.df = pd.DataFrame(self.leader_json)
        return self.df

    def to_json(self):
        """
        Convert the scraped data to JSON format.
        """
        self.result = self.df.to_json(orient="index")
        self.parsed = loads(self.result)

    def save_data(self, filetype: str):
        """
        Save the scraped data to the specified file type.

        Args:
        - filetype (str): The type of file to save (json, excel, or csv).
        """
        self.filetype = filetype
        if self.filetype == "excel":
            self.outputdf.to_excel('leaders.xlsx')
        elif self.filetype == "json":
            self.to_json()
            with open("leaders.json", "w") as file:
                json.dump(self.parsed, file, indent=4)
        elif self.filetype == 'csv':
            self.outputdf.to_csv('leaders.csv')
        else:
            print('Enter a valid filetype: json, csv, or excel')

    def multiple_countries(self, country_list: list):
        """
        Scrape information for multiple countries and concatenate the results.

        Args:
        - country_list (list): List of country codes.

        Returns:
        - pd.DataFrame: Concatenated DataFrame of leader information.
        """
        self.outputdf = pd.DataFrame()  # Initialize an empty DataFrame
        for country in country_list:
            self.get_leaders(country)
            self.into_dataframe()
            self.outputdf = pd.concat([self.outputdf, self.df], ignore_index=True)  # Assign the result back to self.outputdf
        return self.outputdf

    def country_selector(self):
        """
        Allow the user to select countries.

        Returns:
        - list: List of selected country codes.
        """
        country_list = []
        while True:
            user_input = input("Enter a number or '0' to stop: ")

            if user_input == '0':
                print("Exiting the country selector.")
                break  # Exit the loop if the user enters '0'
            elif user_input in ['1', '2', '3', '4', '5']:
                country_list.append(user_input)
            else:
                print("Invalid input. Please enter a valid number or '0' to stop.")

        return country_list
