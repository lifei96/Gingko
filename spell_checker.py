import html2text
from spellchecker import SpellChecker


def get_text(html):
    '''Extracts text from html.'''
    text_maker = html2text.HTML2Text()
    text_maker.no_wrap_links = True
    text_maker.ignore_links = True
    text_maker.ignore_tables = True
    text_maker.ignore_images = True
    text = text_maker.handle(html)
    return text


def get_spell_score(html):
    '''
    Returns the Flesch-Kincaid Grade of the given text. This is a grade
    formula in that a score of 9.3 means that a ninth grader would be able to
    read the document.
    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch%E2%80%93Kincaid_grade_level
    '''
    text = get_text(html)
    spell = SpellChecker()
    wordset = []
    for line in text.split('\n'):
        for word in line.split():
            if word.isalpha():
                wordset.append(word)
    spell.word_frequency.load_words(['microsoft', 'apple', 'google', 'facebook', 'instagram', 'podcasts'])
    misspelled = spell.unknown(wordset)
#     print(misspelled)
    return 1 - 1.0 * len(misspelled) / len(wordset)


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
            spell_score = get_spell_score(f.read().decode('UTF-8'))
            print('\n' + html_example)
            print("spell score: " + str(spell_score))
    print("\n-----Legit examples-----")
    for html_example in legit_examples:
        with open(html_example, 'r') as f:
            spell_score = get_spell_score(f.read().decode('UTF-8'))
            print('\n' + html_example)
            print("spell score: " + str(spell_score))
