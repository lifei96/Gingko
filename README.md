# Gingko
BigCo Team 14 - SP 2019

Our dataset in SQL format: https://drive.google.com/file/d/1ebdN6rQYocJof_cKpVyLPCq2DR729ekh/view?usp=sharing

## Feature Extractors

All the feature extractors can be found in `extractor_accelerated.py`.

## Text Extractor
* API:
  * `te = TextExtractor(url, local)`
  * `te.getText()`
* Parameters:
  `url`: string
  `local`: `True` by default. For online sites, use `False` instead.

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
