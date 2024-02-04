from src.scraper import WikipediaScraper

def main():
    """
    The main function of the LeaderScraper program.

    This function initializes a WikipediaScraper object, interacts with the user to select
    countries and options, scrapes leader information, and saves the data in a specified format.

    Usage:
    - Run this script to execute the LeaderScraper program.
    """
    # Initialize WikipediaScraper object
    wikiscrap = WikipediaScraper()

    # User prompt for selecting countries
    print('Welcome to LeaderScraper! For which countries would you like to see data about their leaders? \n'
        'to add Belgium, press 1 \n'
        'to add France, press 2 \n'
        'to add Morocco press 3 \n'
        'to add Russia press 4 \n'
        'to add the United States of America press 5 \n'
        'to close the selector, press 0')

    # Get selected countries from the user
    countrylist = wikiscrap.country_selector()

    # Scrape information for the selected countries
    wikiscrap.multiple_countries(countrylist)
    print('Info about leaders of your selected countries is loaded!')

    #wikiscrap.into_dataframe()

    # Option to include short biography for each leader
    bio_flag = input('Do you want to include a short bio for each leader? yes or no.  ')
    if bio_flag == 'yes':
        wikiscrap.append_wiki_bio_multi()
        print('Short biographies are attached!')

    # Choose the file format and save the data
    filetype_flag = input('How do you want to save your file? excel, csv, or json   ')
    wikiscrap.save_data(filetype_flag)
    print(f'Your data is now saved as a {filetype_flag} document called "leaders"')

    exit()

if __name__ == "__main__":
    # Execute the main function if the script is run
    main()
