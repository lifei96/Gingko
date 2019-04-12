import numpy as np

from server.extractor import get_img_number, get_ads_number, get_reading_level,\
    social_media_score, citation_score, sentiment_analysis

mean = np.array([0, 0, 0, 0, 0, 0])
std = np.array([1, 1, 1, 1, 1, 1])


def preprocess(html):
    vec = np.array([get_img_number(html), get_ads_number(html),
                    get_reading_level(html), social_media_score(html),
                    citation_score(html), sentiment_analysis(html)
                    ])
    vec = (vec - mean) / std
    return vec
