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

# we first initialize the CSV file with the appropriate headers
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

# Open the file in write mode
with open(csv_file_path, mode='w', newline='') as file:
    # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerow(csv_headers)


# this defines the URL for individual category pages
init_url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/page-1.html"

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

# we now have a list of URLs for individual book pages in each category
# we loop through these and extract the book information as in phase 1
for book_url in urls:
    url = book_url
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
    number_available = table_content[5].string.split('(')[1].split(' available')[0]
    #there's no identifying marks on the <p> containing the product description so we have to find it from the heading next to it
    product_description = soup.find('div',id='product_description').find_next_sibling().string
    #category is third link that appears on the page
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

    with open(csv_file_path, mode='a', newline='') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerow(book_row)
        

