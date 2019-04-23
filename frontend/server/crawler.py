import os
import hashlib
import urllib3


class Crawler(object):
    URL_CACHE_DIR = 'server/url_cache'

    def __init__(self):
        self.http = urllib3.PoolManager()

    def fetch_single_url(self, url):
        """
        Fetches the html given a url.
        :param url: a url string.
        :return: a tuple of (html, http status code).
        """
        hashed_url = hashlib.sha1(url.encode()).hexdigest()
        url_cache_path = self.URL_CACHE_DIR + '/' + hashed_url + '.html'
        if not os.path.isdir(self.URL_CACHE_DIR):
            os.mkdir(self.URL_CACHE_DIR)
        if os.path.exists(url_cache_path):
            print('Cache exists!')
            with open(url_cache_path, 'r') as f:
                return 200, f.read()
        print('Cache not exists!')
        r = self.http.request('GET', url)
        print('Http request status code: ' + str(r.status))
        html_str = r.data.decode('utf-8')
        if r.status == 200:
            with open(url_cache_path, 'w') as f:
                f.write(html_str)
            print('url cached!')
        return r.status, html_str


if __name__ == '__main__':
    crawler = Crawler()
    crawler.fetch_single_url('https://www.cnn.com')
    crawler.fetch_single_url('https://www.bbc.com')
    crawler.fetch_single_url('https://www.nbc.com')
    crawler.fetch_single_url('https://www.cnn.com')
    crawler.fetch_single_url('https://www.bbc.com')
    crawler.fetch_single_url('https://www.nbc.com')
