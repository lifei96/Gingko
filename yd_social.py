from bs4 import BeautifulSoup
import re

good_references = ['nytimes.com', 'wikipedia.org', 'news.yahoo.com', 'news.google.com', 'huffpost.com', 'cnn.com', 'foxnews.com', 'nbcnews.com', 'dailymail.co.uk', 'washingtonpost.com', 'theguardian.com', 'wsj.com', 'abcnews.go.com', 'bbc.com', 'usatoday.com', 'latimes.com']

# Open a file: file
# file = open("./html_samples/legit/DNA leads to man's arrest.htm", mode='r')
file = open("./html_samples/fake/TRUMP WINS BIG.htm", mode='r')
# read all lines at once
html_page = file.read()
print(html_page)

# close the file
file.close()

def get_social_media_score_links(links):
    social_media_links = set()
    for link in links:
        if len(link) > 50:
            continue
        if "www.facebook.com" in link or "twitter.com" in link or "www.instagram.com" in link:
            social_media_links.add(link)

    return social_media_links

def get_links(html_page):
    soup = BeautifulSoup(html_page)
    links = set()
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.add(link.get('href'))
    for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
        links.add(link.get('href'))

    return links

def secure_link_ratio(links):
    count = 0
    for link in links:
        if "https:" in link:
            count += 1

    return float(count/len(links))

def good_reference_ratio(links):
    count = 0
    for link in links:
        if link in good_references:
            count += 1

    return float(count / len(links))

def social_media_score(html_page):
    """
    Crawl links to social media of HTML page and assess the credibility of the website

    Args:
        html_page (str): stringfied html page.
    Returns:
        a float from 0-1 indicating the credibility score based on social media profile
    """
    links = get_links(html_page)
    social_media_links = get_social_media_score_links(links)
    print(social_media_links)
    return round(float(len(social_media_links)/3), 2)

def citation_score(html_page):
    """
    Crawl external citations of HTML page
    Assess security of links and compare against a manually curated credible news website set

    Args:
        html_page (str): stringfied html page.
    Returns:
        a float from 0-1 indicating the credibility score based on citation security and credibility
    """
    links = get_links(html_page)
    secure_ratio = secure_link_ratio(links)
    ref_ratio = good_reference_ratio(links)
    if ref_ratio == 0.0:
        return  round(secure_ratio, 2)
    else:
        ratio = 1.0 if secure_ratio + ref_ratio > 1.0 else ref_ratio + secure_ratio
        return round(ratio, 2)

links = get_links(html_page)

print("social media score is " + str(social_media_score(html_page)))
print("citation score is " + str(citation_score(html_page)))