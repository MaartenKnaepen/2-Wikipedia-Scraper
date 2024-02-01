import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from json import loads, dumps
import json

main_dict = {1:'be', 2:'fr',3:'ma', 4:'ru',5:'us'}
   
def select_country(key):
    value = main_dict[int(key)]
    return value

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

    def get_leaders(self, cntry) -> None:
        self.leader_country_endpoint = self.leaders_endpoint + '?country=' + cntry
        self.leader = requests.get(self.leader_country_endpoint, cookies=self.cookie)
        self.dict_lst = ['id','first_name','last_name','birth_date','death_date','place_of_birth','wikipedia_url','start_mandate', 'end_mandate']
        self.leader_json = self.leader.json()
        for a in self.dict_lst:
            self.leaders_data[a] = [self.leader_json[i][a] for i in range(len(self.leader_json))]
        
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
        for url in self.leaders_data['wikipedia_url']:
            self.paragraph = self.get_first_paragraph(url)
            bio.append(self.paragraph)
        self.leaders_data['biography'] = bio

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
            elif self.filetype == 'csv':
                with open('dict.csv', 'w') as csv_file:  
                    writer = csv.writer(csv_file)
                    for key, value in mydict.items():
                        writer.writerow([key, value])
            else:
                print('Enter a valid filetype, json or excel')
    
    def __repr__(self) -> str:
        return "This is a WikipediaScraper object."

wikiscrap = WikipediaScraper()
wikiscrap.get_leaders('ru')