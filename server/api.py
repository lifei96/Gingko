import pickle

from crawler import Crawler
from preprocess import preprocess

crawler = Crawler()

MODEL_PATH = 'models/final_model.pickle'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)


def get_score(url):
    """
    Gets the scores for a given url.
    :param url: the given url.
    :return: a json containing sub-scores and the total score.
    """
    try:
        http_status_code, html_str = crawler.fetch_single_url(url)
        feature_vector = preprocess(html_str)
        total_score = model.predict(feature_vector)
        return [
            {"id": "Credibility", "score": (1.0 - total_score) * 100},
            {"id": "Number of Images", "score": 100 - max(min(feature_vector[0] / 10, 100), 0)},
            {"id": "Number of Ads", "score": 100 - max(min(feature_vector[1], 100), 0)},
            {"id": "Reading Level", "score": 100 - max(min(feature_vector[2] / 10, 100), 0)},
            {"id": "Social Network Links", "score": max(min(feature_vector[3] * 10, 100), 0)},
            {"id": "Cross-site Citations", "score": max(min(feature_vector[4] * 100, 100), 0)},
            {"id": "Sentiment", "score": max(min(feature_vector[5] * 100, 100), 0)},
        ]
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)
        return []


if __name__ == '__main__':
    print(get_score(
        'https://www.cnn.com/2019/04/11/politics/immigrant-detainees-sanctuary-cities/index.html'))
    print(get_score(
        'https://www.wsj.com/articles/for-50-million-book-your-vacation-in-space-11554994767?mod='
        'foesummaries'))
