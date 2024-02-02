from src.scraper import WikipediaScraper

def main():
    wikiscrap = WikipediaScraper()
    print('Welcome to LeaderScraper! For which countries would you like to see date about their leaders? \n'
        'to add Belgium, press 1 \n'
        'to add France, press 2 \n'
        'to add Morocco press 3 \n'
        'to add Russia press 4 \n'
        'to add the United States of America press 5 \n'
        'to close the selector, press 0')
    countrylist = wikiscrap.country_selector()

    wikiscrap.multiple_countries(countrylist)
    print('Info about leaders of your selected countries is loaded!')

    bio_flag = input('Do you want to include a short bio for each leader? yes or no.  ')
    if bio_flag =='yes':
        wikiscrap.append_wiki_bio()
    print('Short biographies are attached!')
    filetype_flag = input('How do you want to save your file? excel, csv or json   ')
    wikiscrap.save_data(filetype_flag)
    print(f'Your data is now saved as a {filetype_flag} document called "leaders"')

    exit()

if __name__ == "__main__":
    main()