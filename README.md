# Gingko
BigCo 14 - SP 2019

Larger dataset in SQL format: https://drive.google.com/file/d/1ebdN6rQYocJof_cKpVyLPCq2DR729ekh/view?usp=sharing

spell_checker.py    get_spell_score(html)

reading_level.py    get_reading_level(html)

yd_social.py    social_media_score(html)    citation_score(html_page)


## Text Extractor
* API:
  * `te = TextExtractor(url, local)`
  * `te.getText()`
* Parameters:
  `url`: string
  `local`: default=True, for online sites, fill in with False.

```
    # Online request example
    url = 'https://www.nytimes.com/2019/03/14/us/politics/mueller-report-public.html?action=click&module=Top%20Stories&pgtype=Homepage'
    te = TextExtractor(url, local=False)
    print(te.getText())
    
    # Local html file example
    dir = './html_samples/legit/DNA leads to man\'s arrest.htm'
    te = TextExtractor(dir)
    print(te.getText())
   ```

## Plot Density
* API:
  * ```
    from plot_density import *
    plot_hist(data, hist=True, kde=False)
    ```
    
## Sentimental Analysis
* API:
  * `sentiment_analysis(url, local=False, full_score=False)`
* Example:
  * sentiment_analysis('www.google.com')
  * sentiment_analysis('./some_cache.html', local=True)
* For tests, run `sentiment.py` directly or use
  * ```
    print('# ------------ Full sentiment analysis test ------------ #')
    database_test_sentiment_analysis_full()

    print('# -------- Single score sentiment analysis test -------- #')
    database_test_sentiment_analysis()
    ```
