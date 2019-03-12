import textstat
import html2text


def get_text(html):
    '''Extracts text from html.'''
    return html2text.html2text(html)


def get_reading_level(html):
    '''
    Returns the Flesch-Kincaid Grade of the given text. This is a grade
    formula in that a score of 9.3 means that a ninth grader would be able to
    read the document.
    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch%E2%80%93Kincaid_grade_level
    '''
    return textstat.flesch_kincaid_grade(get_text(html))


if __name__ == '__main__':
    fake_examples = [
        "./html_samples/fake/TRUMP WINS BIG.htm",
        "./html_samples/fake/Kentucky Representative Kills Himself.htm",
        "./html_samples/fake/Trojan Name New Ultra-Thin Skin Condom after Donald Trump.htm",
        "./html_samples/fake/Women Abandon Feminism.htm",
    ]
    legit_examples = [
        "./html_samples/legit/Bernie Sanders raises $4 million in less than 1 day of presidential campaign.htm",
        "./html_samples/legit/DNA leads to man's arrest.htm",
        "./html_samples/legit/Mueller probe 'near the end game'.htm",
    ]
    print("-----Fake examples-----")
    for html_example in fake_examples:
        with open(html_example, 'r') as f:
            reading_level = get_reading_level(f.read())
            print('\n' + html_example)
            print("Reading level: " + str(reading_level))
    print("\n-----Legit examples-----")
    for html_example in legit_examples:
        with open(html_example, 'r') as f:
            reading_level = get_reading_level(f.read())
            print('\n' + html_example)
            print("Reading level: " + str(reading_level))
