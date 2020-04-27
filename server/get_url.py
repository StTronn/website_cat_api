#export get_content
import ssl
from urllib.request import Request, urlopen
from inscriptis import get_text
import html2text


from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
import nltk
english_words = set(words.words())

ERROR_MSG = "UNABLE TO CATEGORISE URL"
MIN_REQ = 10
#frequent insignificant words
AVOID = ['browser', 'javascript', 'failed', 'load', 'contact', 'contacts', 'older', 'home', 'more', 'version', 'main', 'menu', 'sign', 'log', 'account', 'content', 'navigate', 'blocked', 'supported', 'support', 'unsupported',  'enable', 'disable', 'register', 'navigation', 'skip', 'jump', 'section', 'policy', 'site', 'uses', 'cookies', 'cookie' 'upgrade', 'anymore',  'required', 'enabled', 'disabled', 'copyright', 'rights', 'copyrights', 'terms',  'conditions', 'privacy', 'policies', 'best']


def lemmatize(text):
    return (WordNetLemmatizer().lemmatize(text))

def is_english(text):
  """ Need to upgrade for checking valid words """

  return text in english_words


def preprocess(content):
  """  1) tokenization
       2) remove stopwords or word with non-alphabetic character or word with length less than 3
       3) converte in lowercase
       4) lemmatization
       5) remove frequent insignificant words """

  content = simple_preprocess(content, deacc=True, min_len=4, max_len=45)
  content = [lemmatize(token) for token in content if token not in STOPWORDS and token not in AVOID]
  content = list(filter(lambda word: is_english(word), content))
  if len(content) >= MIN_REQ: return content
  else: raise


def get_text_content(url):
  """ return all text content from url """

  req = Request(url, headers={'User-Agent': 'Mozilla/75.0'})
  uvcontext = ssl._create_unverified_context()
  webpage = urlopen(req,context=uvcontext).read().decode('utf-8')
  return get_text(webpage)

def get_content(url):
    return preprocess(get_text_content(url))

