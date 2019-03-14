import re
import urllib.request
import codecs
from bs4 import BeautifulSoup

class TextExtractor():
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text/1983219#1983219
    
    def __init__(self, url, local=True):
        if local:
            html = open(url, 'r', encoding='utf-8', errors='ignore')
        else:
            html = urllib.request.urlopen(url).read()

        self.data = BeautifulSoup(html, 'html5lib').findAll(text=True)
     
    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'li', 'ul', 'button']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True
    
    def getText(self):
        text = filter(self.visible, self.data)
        result = ''
        for line in list(text):
            if len(line.split()) > 0:
                result += line.strip()
                result += ' '
        return result

if __name__ == '__main__':
    # Online request example
    url = 'https://www.nytimes.com/2019/03/14/us/politics/mueller-report-public.html?action=click&module=Top%20Stories&pgtype=Homepage'
    te = TextExtractor(url, local=False)
    print(te.getText())
    
    # Local html file example
    dir = './html_samples/legit/DNA leads to man\'s arrest.htm'
    te = TextExtractor(dir)
    print(te.getText())