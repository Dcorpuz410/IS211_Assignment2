import urllib.request
import logging
import datetime
import argparse

# url = 'http://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
# Create a logger object
logger = logging.getLogger(__name__)

def download_data(url):
    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return: the content of the URL
    """
    # read the URL
    response = urllib.request.urlopen(url)

    # return the data
    return response.read().decode('utf-8')

def process_data(file_content):
    """Processes the data"""
    person_data = {}
    lines = file_content.splitlines()
    for line in lines:
        line = line.rstrip('\n')
        person = line.split(',')
        if len(person) >= 3:
            try:
                id = int(person[0])
                name = person[1]
                birthday = datetime.datetime.strptime(person[2], '%Y/%m/%d')
            except ValueError:
                logger.error(f"Error processing line: {line}")
            else:
                person_data[id] = (name, birthday)
    return person_data

def display_person(id, person_data):
    """Displays the person"""
    if id in person_data:
        print(f"Person {id} is {person_data[id][0]} with a birthday of {person_data[id][1]}")
    else:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")
    csv_data = download_data(url)
    person_data = process_data(csv_data)
    while True:
        try:
            id = int(input("Enter an ID number: "))
            if id <= 0:
                break
            display_person(id, person_data)
            print('Type "0" to quit')
        except ValueError:
            print("Invalid input. Please enter a valid ID number.")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)