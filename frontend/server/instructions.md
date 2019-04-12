## Environment

We tested this program with Python 3.6 environment. Python 2 is not recommended, since some of the dependencies only work with Python 3.

## Package dependency

To run this program, first use pip to install the following packages.
```
pip install textstat 
pip install html2text 
pip install nltk 
pip install beautifulsoup4 
pip install catboost
```

In case of any problems, more detailed documentations can be found at 
* [textstat](https://github.com/shivam5992/textstat)
* [html2text](https://pypi.org/project/html2text/)
* [nltk](https://www.nltk.org/install.html)
* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Sample
```
from preproc import *
html = 'some raw html string'
feature_vec = preproc(html)
```
