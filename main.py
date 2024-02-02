from src.scraper import WikipediaScraper

def main():
    """
    The main function of the LeaderScraper program.

    This function initializes a WikipediaScraper object and provides a user interface for
    interacting with the scraping functionality to retrieve information about country leaders.

    Usage:
    - Run this script to execute the LeaderScraper program.
    """
    wikiscrap = WikipediaScraper()  # Initialize outside the loop

    while True:
        print('\nWelcome to LeaderScraper! \n'
              'For available countries, press 1 \n'
              'For info about leaders of all countries, press 2 \n'
              'To close this program, press 3')

        user_input = input('Enter your choice: ')

        if int(user_input) == 1:
            # Display available countries
            print(f'Available countries are: {wikiscrap.get_countries()}')

        elif int(user_input) == 2:
            # Scraping and saving leaders' information
            print('Go get a coffee. This will take a while.')
            wikiscrap.get_leaders()
            wikiscrap.save_data('json', 'leaders')
            print('Data collection was successful! The output is saved in the file leaders.json')
        elif int(user_input) == 3:
            # Exit the program
            exit()
        else:
            # Handle invalid input
            print('Please enter a valid number')

if __name__ == "__main__":
    # Execute the main function if the script is run
    main()
