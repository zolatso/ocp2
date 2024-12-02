from bs4 import BeautifulSoup
import requests
import csv
import os
from phase1 import csv_headers, scrape_book
from phase2 import get_books_from_category
from phase3 import get_category_url_and_name, create_csv, create_dir



# function that downloads individual images
def download_image(dir, image_url, f_name):
    f_name = f_name+'.jpg'
    full_name = os.path.join(dir+'/images', f_name)
    with open(full_name, mode='wb') as file:
        file.write(requests.get(image_url).content)


        
if __name__ == '__main__':

    list_of_cats = get_category_url_and_name("https://books.toscrape.com/index.html")

    for name, url in list_of_cats.items():

        category_dir = create_dir(name)
        get_book_urls = get_books_from_category(url)
        book_rows = []
        for book_url in get_book_urls:
            book_row = scrape_book(book_url)
            book_rows.append(book_row)
            download_image(category_dir, book_row[9], book_row[1])
        
        create_csv(category_dir, name, book_rows)

    