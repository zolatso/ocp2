from bs4 import BeautifulSoup
import requests
import csv
from phase1 import scrape_book, csv_headers


def write_books_to_csv(book_rows, csv_file_path):
    # Open the file in write mode
    with open(csv_file_path, mode='w', newline='') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerow(csv_headers)
        writer.writerows(book_rows)

def get_books_from_category(init_url):

    # extract html from initial url
    response = requests.get(init_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    # we work from the ol element that contains a list of all the books on that page
    list_of_book_links = soup.find('ol',{'class':'row'}).find_all('li')
    urls = []
    for book_link in list_of_book_links:
        # extract the link from the a tag and remove the relative directory characters
        link = book_link.a.attrs.get('href')[9:]
        link = 'https://books.toscrape.com/catalogue/'+link
        # place individual links in a list we will iterate through later
        urls.append(link)

    # after extracting links to books, checks if there is a link to a next page
    next_page = soup.find('li',{'class':'next'})

    # cycles through the different pages and extracts their URLs
    while next_page:

        #extract the actual link from the a tag contained within the list item
        next_page_name = next_page.a.attrs.get('href')

        # these three lines are needed because the extracted link does not include the full url
        page_name = init_url.split('/')
        length_of_page_name = len(page_name[-1])
        base_url = init_url[:-length_of_page_name]  
        next_page_url = base_url + next_page_name

        response = requests.get(next_page_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        # repeat the loop from above
        list_of_book_links = soup.find('ol',{'class':'row'}).find_all('li')
        for book_link in list_of_book_links:
            # extract the link from the a tag and remove the relative directory characters
            link = book_link.a.attrs.get('href')[9:]
            link = 'https://books.toscrape.com/catalogue/'+link
            # place individual links in a list we will iterate through later
            urls.append(link)

        # reassign the next_soup variable before checking if its true at the start of the while loop
        next_page = soup.find('li',{'class':'next'})

    return urls


if __name__ == '__main__':

    get_urls = get_books_from_category("https://books.toscrape.com/catalogue/category/books/fantasy_19/page-1.html")
    book_rows = []
    for book_url in get_urls:
        book_row = scrape_book(book_url)
        book_rows.append(book_row)
    
    write_books_to_csv(book_rows, 'example.csv')

