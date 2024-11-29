from bs4 import BeautifulSoup
import requests
import csv
import os

# function that creates a new CSV file. Parameter should be name of category, used for the file name
# it puts it inside a folder named after the category
# it also then creates a folder for the images within this
def create_csv(file_name):
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

    # creates a new folder inside local directory
    # this is where we store the csv and individual images for each category
    current_folder = os.getcwd()
    new_folder = file_name
    new_path = os.path.join(current_folder, new_folder)
    images_folder = 'images'
    # make this variable global as it will be needed in the image downloader
    global new_images_folder 
    new_images_folder = os.path.join(new_path, images_folder) 
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    if not os.path.isdir(new_images_folder):
        os.mkdir(new_images_folder)
    

    # File path for the CSV file
    csv_file = file_name+'.csv'
    csv_file_path = os.path.join(new_path, csv_file)

    # Open the file in write mode
    with open(csv_file_path, mode='w', newline='', encoding="utf-8") as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerow(csv_headers)
    
    # return the file path as we will need this to add each book to the csv file
    return csv_file_path

# function that downloads individual images
def download_image(image_url, f_name):
    f_name = f_name+'.jpg'
    full_name = os.path.join(new_images_folder, f_name)
    with open(full_name, mode='wb') as file:
        file.write(requests.get(image_url).content)

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


whole_site_url = "https://books.toscrape.com/index.html"
response = requests.get(whole_site_url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

list_of_cats = soup.find('div', {'class':'side_categories'}).find_next('ul').find_next('ul').find_all('li')

all_cats = {}
for item in list_of_cats:
    category_name = item.a.string.strip().lower()
    category_url = 'https://books.toscrape.com/'+item.a.attrs.get('href')
    all_cats[category_name] = category_url

for name, url in all_cats.items():
    csv_file = create_csv(name)
    # this defines the URL for individual category pages
    init_url = url

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
        #also, occcasionally the product description field doesn't exist, so we have to check that with an if
        if soup.find('div',id='product_description'):
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

        # put relevant variables in a list
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

        #write the list to the csv file created earlier on
        with open(csv_file, mode='a', newline='') as file:
            # Create a csv.writer object
            writer = csv.writer(file)
            # Write data to the CSV file
            writer.writerow(book_row)
        
        # download each image
        download_image(full_url, upc)
        
    
