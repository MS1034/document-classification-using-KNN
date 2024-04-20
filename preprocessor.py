from spellchecker import SpellChecker
from collections import Counter
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from text_preprocessing import preprocess_text, expand_contraction, remove_email, remove_phone_number, remove_special_character, remove_itemized_bullet_and_numbering, normalize_unicode, substitute_token
from nltk.tokenize import word_tokenize

PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()


def tokenize(text):
    return word_tokenize(text)


def lowercase_text(text):
    return text.lower()


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    clean_text = url_pattern.sub('', text)
    return clean_text


def remove_punctuation(text):
    return ' '.join(text.translate(str.maketrans('', '', PUNCT_TO_REMOVE)).split())


def remove_whitespace(text):
    return ' '.join(text.split())


def remove_stopwords(text):
    return ' '.join([word for word in str(text).split() if word not in STOPWORDS])


def lemmatize_words(text):
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def stem_words(text):
    return " ".join([stemmer.stem(word) for word in text.split()])


def part_of_speech_tagging(text):
    result = TextBlob(text)
    return result.tags


def remove_words_above_threshold(text, threshold=5):
    tokens = word_tokenize(text)
    word_freq = Counter(tokens)

    filtered_words = [word for word in tokens if word_freq[word] >= threshold]

    return ' '.join(filtered_words)


def remove_frequent_words(tokens, top_n=10):
    word_freq = Counter(tokens)
    frequent_words = set([word for word, _ in word_freq.most_common(top_n)])
    filtered_tokens = [word for word in tokens if word not in frequent_words]
    return filtered_tokens


def remove_emoticons(text):
    emoticon_pattern = r'(?::|;|=)(?:-)?(?:\)|\(|D|P)'
    text_without_emoticons = re.sub(emoticon_pattern, '', text)
    return text_without_emoticons


def correct_spellings(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        corrected_word = spell.correction(word)
        if corrected_word is not None:
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)


def text_preprocessing(text):

    text = expand_contraction(text)
    text = remove_email(text)
    text = remove_special_character(text)
    text = remove_phone_number(text)
    text = normalize_unicode(text)
    text = remove_html_tags(text)
    text = remove_numbers(text)
    text = remove_urls(text)
    text = remove_emoticons(text)
    text = remove_emoji(text)
    text = lowercase_text(text)
    text = remove_punctuation(text)
    text = remove_whitespace(text)
    text = remove_stopwords(text)
    text = stem_words(text)
    text = lemmatize_words(text)
    text = correct_spellings(text)
    text = remove_itemized_bullet_and_numbering(text)

    return text
