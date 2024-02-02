from src.scraper import WikipediaScraper, select_country

def main():
    k = 0
    while k != 6:
        k = input('Welcome to LeaderScraper! For which countries would you like to see date about their leaders? \n'
            'for Belgium, press 1 \n'
            'for France, press 2 \n'
            'for Morocco press 3 \n'
            'for Russia press 4 \n'
            'for the United States of America press 5 \n'
            'for all countries press 6 \n'
            'to close this program, press 7  ')
        wikiscrap = WikipediaScraper()
        if int(k) == 7:
            exit()
        elif int(k) < 6:
            cntry = select_country(k)
            wikiscrap.get_leaders(cntry)
        
        wikiscrap.into_dataframe()
        bio_flag = input('Do you want to include a short bio for each leader? yes or no.  ')
        if bio_flag =='yes':
            wikiscrap.append_wiki_bio()
        filetype_flag = input('How do you want to save your file? excel, csv or json   ')
        wikiscrap.save_data(filetype_flag)

if __name__ == "__main__":
    main()