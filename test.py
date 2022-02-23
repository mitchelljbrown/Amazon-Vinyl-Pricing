from bs4 import BeautifulSoup
from matplotlib.pyplot import text
import requests
import pandas as pd

album = []
artist = []
rating = []
price = []

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        

url = "https://www.amazon.ca/gp/bestsellers/music/1292212011/ref=s9_acss_bw_cg_vinyl_3a1_w?pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-3&pf_rd_r=04Y3C47WF3J5AMC6NRZ7&pf_rd_t=101&pf_rd_p=e647b509-1d9d-4abc-80c7-7c085f4e9577&pf_rd_i=1292212011"
html_text = requests.get(url, headers=HEADERS).text

soup = BeautifulSoup(html_text, 'lxml')
records = soup.find_all('div', id ='gridItemRoot')
for record in records:
    album_name = record.find('div', class_='_p13n-zg-list-grid-desktop_truncationStyles_p13n-sc-css-line-clamp-1__1Fn1y').text
    album.append(album_name)
    artist_name = record.find('span', class_='a-size-small a-color-base').text
    artist.append(artist_name)
    # if 'a-icon-row' in record:
    #     record_rating = record.find('div', class_='a-icon-row').text.split(' ')[0]
    #     rating.append(record_rating)
    # else:
    #     rating.append('NA')

#record_rating = records[10].find('div', class_='a-icon-row').text.split(' ')[0]

    

#print(len(record))
print(len(album))
print(len(artist))
#print(artist)



