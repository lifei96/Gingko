# Gingko
BigCo 14 - SP 2019

Larger dataset in SQL format: https://drive.google.com/file/d/1ebdN6rQYocJof_cKpVyLPCq2DR729ekh/view?usp=sharing

spell_checker.py    get_spell_score(html)

reading_level.py    get_reading_level(html)

yd_social.py    social_media_score(html)    citation_score(html_page)


## Text Extractor
* API:
  > te = TextExtractor(url, local)
  > te.getText()
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
