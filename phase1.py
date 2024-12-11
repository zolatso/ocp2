from bs4 import BeautifulSoup
import requests
import csv

#This function deals with the rating category which is written as a word; integer more useful
def convert_word_to_num(num):
    numberList = {
        'One':1,
        'Two':2,
        'Three':3,
        'Four':4,
        'Five':5
    }
    if num in numberList:
        return numberList[num]
    else:
        return num

def scrape_book(url):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    product_page_url = url
    # Some of the required information is inside a table, so we find all the table cells
    # Remove the html tags and put them in a list
    table_content = soup.find_all('td')
    upc = table_content[0].string
    title = soup.find('h1').string
    price_excluding_tax = table_content[2].string
    price_including_tax = table_content[3].string
    #For the number_available we cut off everything apart from the number
    number_available = table_content[5].string[10:].split()[0]
    # there's no identifying marks on the <p> containing the product description so we have to find it from the heading next to it
    product_description = soup.find('div',id='product_description').find_next_sibling().string
    # category is third link that appears on the page
    category = soup.find_all('a')[3].string
    # Extracting the rating: it is located in the class name of the <p> tag containing the stars
    star_rating = convert_word_to_num(soup.find('p',{'class':'star-rating'}).attrs.get('class')[1])
    # image url includes a relative link so I've replaced the first directories with the full address just in case
    image_url = soup.find('img').attrs.get('src')[5:]
    base_url = 'https://books.toscrape.com'
    sequence = (base_url, image_url)
    full_url = ''.join(sequence)

    book_row = [
        product_page_url,
        upc,
        title,
        price_excluding_tax,
        price_including_tax,
        number_available,
        product_description,
        category,
        star_rating,
        full_url
    ]
    return book_row

csv_headers = [
    'product_page_url',
    'universal_product_code (upc)',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
]

# File path for the CSV file
csv_file_path = 'example.csv'

def download_book(book_row):
    with open(csv_file_path, mode='a', newline='') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        writer.writerow(csv_headers)
        # Write data to the CSV file
        writer.writerow(book_row)

if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
    book_row = scrape_book(url)
    download_book(book_row)