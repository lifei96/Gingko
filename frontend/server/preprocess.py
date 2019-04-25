import numpy as np

from server.extractor import get_img_number, get_ads_number, get_reading_level,\
    social_media_score, citation_score, sentiment_analysis

mean = np.array([37.047085, 3.43, 72.53694, 0.70955294, 0.6189926, 0.9909184])
std = np.array([1.0050670e+02, 1.4240866e+01, 1.5686197e+02,
                8.7423748e-01, 3.5920843e-01, 1.0152975e-02])


def preprocess(html):
    vec = np.array([get_img_number(html), get_ads_number(html),
                    get_reading_level(html), social_media_score(html),
                    citation_score(html), sentiment_analysis(html)
                    ])
    vec = (vec - mean) / std
    return vec
