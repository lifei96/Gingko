from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import math
import pymysql
import pymysql.cursors


def sentiment_analysis(text, full_score=False):
    sia = SIA()
    score = sia.polarity_scores(text)
    if full_score:
        return score
    else:
        x = score['neu'] * 5 - abs(score['neg'] - score['pos'])
        x = (x-4.69097597875388)/0.15841387076450403
        return 1/(1 + math.exp(-x))

def example_sentiment_analysis(url):
    te = TextExtractor(url, local=False)
    print(sentiment_analysis(te.getText()))
	


def database_test_sentiment_analysis_full():
    
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='gingko')
    cursor = conn.cursor()
    cursor.execute('select site, is_fake, html from web_pages')
    webs = cursor.fetchall()
    
    neu = [[], []]
    pos = [[], []]
    neg  = [[], []]
    for w in webs:
        neu[w[1]].append(sentiment_analysis(w[2], full_score = True)['neu'])
        pos[w[1]].append(sentiment_analysis(w[2], full_score = True)['pos'])
        neg[w[1]].append(sentiment_analysis(w[2], full_score = True)['neg'])
    
    print('# --------- Neutral -------- #')
    plot_hist(neu, False, True)
    print('# -------- Negative -------- #')
    plot_hist(neg, False, True)
    print('# -------- Positive -------- #')
    plot_hist(pos, False, True)

def database_test_sentiment_analysis():
    
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',db='gingko')
    cursor = conn.cursor()
    cursor.execute('select site, is_fake, html from web_pages')
    webs = cursor.fetchall()
    
    score = [[], []]
    for w in webs:
        score[w[1]].append(sentiment_analysis(w[2]))
    
    print('# --------- Score -------- #')
    plot_hist(score, False, True)
    return score
	
if __name__ == '__main__':
    print('# --------- Example: http://www.mrbottles.com/ --------- #')
    url = 'http://www.mrbottles.com/'
    example_sentiment_analysis()
    
    print('# ------------ Full sentiment analysis test ------------ #')
    database_test_sentiment_analysis_full()
    
    print('# -------- Single score sentiment analysis test -------- #')
    database_test_sentiment_analysis()