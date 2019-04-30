import numpy as np
from bs4 import BeautifulSoup

from server.extractor import get_img_number, get_ads_number, get_reading_level,\
    social_media_score, citation_score, sentiment_analysis

mean = np.array([35.91339874267578, 3.4475998878479004, 67.10360717773438, 0.6936891674995422,
                 0.6221207976341248, 0.9910552501678467])
std = np.array([96.64471435546875, 14.680747985839844, 138.3404998779297, 0.8288413286209106,
                0.35737043619155884, 0.0016996299382299185])


def preprocess(html):
    soup = BeautifulSoup(html, 'html.parser')
    vec = np.array([get_img_number(soup), get_ads_number(soup),
                    get_reading_level(html), social_media_score(soup),
                    citation_score(soup), sentiment_analysis(html)
                    ])
    vec = (vec - mean) / std
    return vec
