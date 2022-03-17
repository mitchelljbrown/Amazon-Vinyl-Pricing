import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import pandas as pd

def get_url(search_term):
    """Generate a url form search term"""
    template = 'https://www.amazon.ca/s?k={}&crid=37IVLUCOF5I3G&sprefix={}%2Caps%2C142&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    # add page number
    url = template.format(search_term, search_term)

    # add page query placeholder
    url += '&page={}'

    return url

# fucntion to extract data from item 
def get_data(item):
    
    search = item.h2.a
    search.text    
    title = search.text.strip()
    
    url = 'https://www.amazon.ca' + search.get('href')
    
    # error handling
    try:
        price = item.find('span', 'a-offscreen').text[1:]
    except AttributeError:
        return
    
    try:
        rating = item.i.text.split(" ")[0]
        review_count = item.find('span', class_='a-size-base s-underline-text').text
    except AttributeError:
        rating=''
        review_count=''

    result = (title, price, rating, review_count, url)

    return(result)

def scrape(search_term):
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    records = []
    url = get_url(search_term)

    for page in range(1, 5):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = get_data(item)
            if record:
                records.append(record)

    driver.close()

    return records

# perform scraping using 
data = scrape('tv')

# covert to DataFrame
data = pd.DataFrame(data)

# set columns
data.columns = ["Item", "Price", "Rating", "Num_Reviews", "URL"]

# save to .csv
data.to_csv("amazon_data.csv")

# print first 5 rows of data
data.head()