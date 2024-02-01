import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from json import loads, dumps
import json

class WikipediaScraper:
    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = self.base_url + '/countries'
        self.leaders_endpoint = self.base_url + '/leaders'
        self.cookies_endpoint = self.base_url + '/cookie'
        self.leaders_data = {}
        self.cookie = requests.get(self.cookies_endpoint).cookies
        self.df = None
        self.leader_json = None
    
    def refresh_cookie(self):
        self.cookie = requests.get(self.cookies_endpoint).cookies
        print('New cookie created!')
    
    def get_countries(self):
        self.countries = requests.get(self.country_endpoint, cookies = self.cookie)
        print(f"The retrieved countries are: {self.countries.text}")

    def get_leaders(self, country: str) -> None:
        if country in ["ma","us","fr","be","ru"]:
            self.country = '?country=' + country
        self.leader_country_endpoint = self.leaders_endpoint + self.country
        self.leader = requests.get(self.leader_country_endpoint, cookies=self.cookie)
        self.leader_json = self.leader.json()
        return self.leader_json

    def get_first_paragraph(self, wikipedia_url: str) -> str:
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
  
    def append_wiki_bio(self):
        bio = []
        for url in self.df['wikipedia_url']:
            self.paragraph = self.get_first_paragraph(url)
            bio.append(self.paragraph)
        self.df['biography'] = bio

    def into_dataframe(self):
        self.df = pd.DataFrame(self.leader_json)

    def to_json(self):
            self.result = self.df.to_json(orient="index")
            self.parsed = loads(self.result)
            self.dumps = dumps(self.parsed, indent=4)  

    def save_data(self, filetype):
            self.filetype = filetype
            if self.filetype == "excel":
                self.df.to_excel('leaders.xlsx')
            elif self.filetype == "json":
                self.to_json()
                with open("leaders.json", "w") as file:
                    json.dump(self.dumps, file)
            else:
                print('Enter a valid filetype, json or excel')
    

wikiscrap = WikipediaScraper()
wikiscrap.get_leaders('ma')
wikiscrap.into_dataframe()
wikiscrap.append_wiki_bio()
wikiscrap.save_data('excel')