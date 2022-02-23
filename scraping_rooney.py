from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
url = "https://www.amazon.ca/s?rh=n%3A1292212011&fs=true&ref=lp_1292212011_sar"

def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getnextpage(soup):
    page = soup.find('url', {'class': 'a-pagination'})
    if not page.find('li', {'class': 'a-disabled a-last'}):
        url = 'http://www.amazon.'

print(getdata())