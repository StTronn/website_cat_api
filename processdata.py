""" consist routines for finding word embeddings, sentence embeddings, sentence
    preprocessing etc """

from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import tokenize
from nltk import FreqDist
import pandas as pd
import numpy as np

PATH = ''

#Dictionary
print('loading dictionary...')
df = pd.read_csv(PATH + 'dictionary.csv')
dictionary = set([row[0] for row in df.values.tolist()])

#Lemmatization
print('loading words lemma...')
df = pd.read_csv(PATH + 'lemmatization.csv')
lemma = {row[0]:row[1] for row in df.values.tolist()}

del df

#Frequent Terms find on web
AVOID = {'error', 'enable', 'jump', 'rights', 'block', 'condition', 'javascript', 'fail', 'menu', 'filipino', 'register', 'site', 'request', 'dutch', 'espanol', 'reserved', 'help', 'home', 'url', 'italiano', 'page', 'navigate', 'cookie', 'browser', 'disable', 'cancel', 'unsupported', 'english', 'francais', 'login', 'privacy', 'term', 'section', 'disabled', 'skip', 'main', 'copyright', 'uses', 'navigation', 'more', 'anymore', 'log', 'open', 'homepage', 'corona', 'policy', 'content', 'terms', 'sign', 'upgrade', 'portugal', 'older', 'require', 'know', 'indonesia', 'support', 'results', 'language', 'coronavirus', 'best', 'load', 'deutsch', 'cookies'}


def lemmatize(word):
  """ param -: str  
      return -: return lemmatize form of word, taking word_2_vec similarity in account to avoid change in meaning """

  return lemma.get(word, word)


def is_significant(word):
  """param -: str 
     return -: True for string b/w length 4 and 45 as well as capitalize 2 or 3 char strings """

  if not word.isalpha(): return False
  if len(word) < 2 or len(word) > 45: return False
  if (len(word) == 3 or len(word) == 2) and not word.isupper(): return False
  return True


def is_english_word(word):
  """ check whether word has all english alphabets """

  for ch in word:
    if ch < 'a' or ch > 'z':
      return False
  return True


def is_english(content):
  """ return True if more than 50% words are english """
  
  cnt = 0
  for word in content:
    if is_english_word(word): cnt += 1
  
  if cnt*2 >= len(content): return True
  else: return False


def preprocess(content):
  """  params -: raw text scrapped from website
       return -: return list of words after:    
                1) tokenization
                2) remove stopwords and some insignificant words
                3) convert in lowercase 
                4) lemmatize 
                5) Remove common web terms """

  content = tokenize(content, deacc=True)
  content = list(filter(is_significant, content))
  content = [token.lower() for token in content]
  MIN_WORDS = 30  #minimum words needed to decide whether site is english or not
  if len(content) > MIN_WORDS and not is_english(content): return ['invalidcontentfound']   #signal for non_engish site 
  content = [lemmatize(token) for token in content if token not in STOPWORDS and token in dictionary]
  content = [token for token in content if token not in AVOID]
  return content