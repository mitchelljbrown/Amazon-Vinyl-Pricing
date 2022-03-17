import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

def get_url(search_term):
    """Generate a url form search term"""
    template = 'https://www.amazon.ca/s?k={}&i=popular&crid=1HNLDFKVIXLLG&sprefix={}%2Cpopular%2C86&ref=nb_sb_noss'
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
    
    try:
        price = item.find('span', 'a-offscreen').text[1:]
    except AttributeError:
        return
    
    try:
        rating = item.i.text.split(" ")[0]
        review_count = item.find('span', class_='a-size-base s-underline-text').text

        artist = item.find('div', class_='a-row a-size-base a-color-secondary').text[3:].split("|")
        
        
        #date = item.find('a', class_='a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold').text[3:].split("|")[1]
        # artist = info[0]
        # year = info[1].replace(" ", "")

        media = item.find('div', class_='a-row a-spacing-mini a-size-base a-color-base').text
    except AttributeError:
        rating=''
        review_count=''
        info=''
        artist=''
        media=''
    except IndexError:
        artist=''
        date=''

    if len(artist) > 1 and artist != '':
        composer = artist[0]
        year = artist[1]
    else:
        composer = artist
        year = ''
    result = (title, composer, year, price, rating, review_count, media, url)

    return(result)

def main(search_term):
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    records = []
    url = get_url(search_term)

    for page in range(1, 399):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = get_data(item)
            if record:
                records.append(record)

    driver.close()

    return records

# Example
#  = main('vinyl records')
vinyl_data = pd.DataFrame(x)
vinyl_data.columns = ["Album", "Artist", "Year", "Price", "Rating", "Reviews", "media", "URL"]
