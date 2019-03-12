from bs4 import BeautifulSoup
import re

def get_img_number(html):
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img')
#     for img in imgs:
#         if img.has_key('height'):
#             print(img['height'])
#         if img.has_key('size'):
#             print(img['size'])
#         if img.has_key('width'):
#             print(img['width'])
    return len(imgs)

def get_ads_number(html):
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img')
    ads_counter = 0
    for img in imgs:
        if "ads" in img['src']:
            ads_counter += 1
    return ads_counter

file = open("./html_samples/fake/TRUMP WINS BIG.htm", mode='r')
html_page = file.read()

print(get_img_number(html_page))
print(get_ads_number(html_page))