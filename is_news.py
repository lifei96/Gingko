from bs4 import BeautifulSoup
import re

def is_news(html):
	news = re.findall('news', html)
	if len(news) > 10:
		return True
	else:
		return False

file = open("./html_samples/fake/Kentucky Representative Kills Himself.htm", mode='r')
html = file.read()
print(is_news(html))
	