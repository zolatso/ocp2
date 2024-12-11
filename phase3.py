from bs4 import BeautifulSoup
import requests
import csv
import os
from phase1 import csv_headers, scrape_book
from phase2 import get_books_from_category


def create_dir(name):
    # function that creates folder for each category and places another folder inside for its images
    # returns the path to the folder
    current_folder = os.getcwd()
    new_folder = 'data'
    cat_folder = name
    new_path = os.path.join(current_folder, cat_folder)
    images = 'images'
    image_path = os.path.join(new_path, images)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
        os.mkdir(image_path)
    return new_path

def create_csv(location, file_name, book_rows):

    # File path for the CSV file
    csv_file = file_name+'.csv'
    csv_file_path = os.path.join(location, csv_file)

    # Open the file in write mode
    with open(csv_file_path, mode='w', newline='', encoding="utf-8") as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerow(csv_headers)
        writer.writerows(book_rows)

def get_category_url_and_name(site_url):

    response = requests.get(site_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    list_of_cats = soup.find('div', {'class':'side_categories'}).find_next('ul').find_next('ul').find_all('li')

    all_cats = {}
    for item in list_of_cats:
        category_name = item.a.string.strip().lower()
        category_url = 'https://books.toscrape.com/'+item.a.attrs.get('href')
        all_cats[category_name] = category_url

    return all_cats

if __name__ == '__main__':

    list_of_cats = get_category_url_and_name("https://books.toscrape.com/index.html")

    for name, url in list_of_cats.items():

        category_dir = create_dir(name)
        get_book_urls = get_books_from_category(url)
        book_rows = []
        for book_url in get_book_urls:
            book_row = scrape_book(book_url)
            book_rows.append(book_row)
        
        create_csv(category_dir, name, book_rows)
    
        
    
