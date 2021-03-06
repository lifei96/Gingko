import pickle

from server.crawler import Crawler
from server.preprocess import preprocess

crawler = Crawler()

MODEL_PATH = 'server/models/final_model.pickle'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

FEATURE_MIN = [-0.37160229682922363, -0.23483815789222717, -0.5985492467880249, -0.8369384407997131,
               -1.7408289909362793, -10.385951042175293]
FEATURE_MAX = [20.219280242919922, 12.230466842651367, 16.901025772094727, 8.815089225769043,
               1.0573879480361938, 1.324949026107788]


def convert_sub_scores(feature_vector):
    return list(map(lambda x: max(min((x[0] - x[1]) / (x[2] - x[1]) * 100, 100), 0),
                    zip(feature_vector, FEATURE_MIN, FEATURE_MAX)))


def get_score(url):
    """
    Gets the scores for a given url.
    :param url: the given url.
    :return: a json containing sub-scores and the total score.
    """
    try:
        http_status_code, html_str = crawler.fetch_single_url(url)
        feature_vector = preprocess(html_str)
        print(feature_vector)
        total_score = model.predict_proba([feature_vector])[0][0]
        # if url == 'https://www.huffpost.com/entry/michelle-obama-pink-suit_n_5caf82f1e4b0ffefe3ad78f4':
        #     return [
        #         {"id": "Credibility", "score": 92},
        #         {"id": "Number of Images", "score": 88},
        #         {"id": "Number of Ads", "score": 76},
        #         {"id": "Reading Level", "score": 84},
        #         {"id": "Social Network Links", "score": 71},
        #         {"id": "Cross-site Citations", "score": 80},
        #         {"id": "Sentiment", "score": 95},
        #     ]
        # else:
        #     return [
        #         {"id": "Credibility", "score": 27},
        #         {"id": "Number of Images", "score": 55},
        #         {"id": "Number of Ads", "score": 20},
        #         {"id": "Reading Level", "score": 15},
        #         {"id": "Social Network Links", "score": 33},
        #         {"id": "Cross-site Citations", "score": 23},
        #         {"id": "Sentiment", "score": 19},
        #     ]
        sub_scores = convert_sub_scores(feature_vector)
        return [
            {"id": "Credibility", "score": int(total_score * 100)},
            {"id": "Number of Images", "score": int(sub_scores[0])},
            {"id": "Number of Ads", "score": int(sub_scores[1])},
            {"id": "Reading Level", "score": int(sub_scores[2])},
            {"id": "Social Network Links", "score": int(sub_scores[3])},
            {"id": "Cross-site Citations", "score": int(sub_scores[4])},
            {"id": "Sentiment", "score": int(sub_scores[5])},
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
