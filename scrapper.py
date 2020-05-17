""" Note -: This Module require chromium-chrome driver to work correctly
            Install using command "apt install chromium-chromedriver"

            consist routines for text scrapping from websites
"""


from bs4 import BeautifulSoup
from bs4.element import Comment
from tldextract import extract
from selenium import webdriver
from timeout import Timeout
import requests
import processdata
import warnings

warnings.filterwarnings("ignore")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
browser.set_page_load_timeout(10)

headers = {
	'User-Agent': 'Mozilla/75.0',
	'Accept-Language': 'en-US,en;q=0.5'
}

SUFFICIENT = 50  #Minimum words require to avoid dynamic content scrapping
MINIMUM = 10 #Minimum content required


def get_status_code(url, default=0):
  """ return status code of url and 0 in case of exception """
  try:
    with Timeout(10):
      res = requests.get(url, headers=headers, verify=False, timeout=3, stream=False)
      return res.status_code
  except:
    return default
  return default


def get_valid_url(url):
  """ return url with valid protocol and status_code """

  if(get_status_code('https://'+url) == 200):
    return {'url':'https://'+url, 'status':200}
  else:
    return {'url': 'http://'+url, 'status': get_status_code('http://'+url)}


def tag_visible(element):
  """ check visible tag """

  if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
      return False
  if isinstance(element, Comment):
      return False
  return True


def text_from_html(html):
  """ Extract visible text from html body """

  soup = BeautifulSoup(html, 'html.parser')
  text = soup.findAll(text=True)
  visible_text = filter(tag_visible, text)  
  return u" ".join(t.strip() for t in visible_text)


def get_about_url(html, url):
  """  return url of about page if exist """
  try:
    domain = extract(url).domain.lower()  #fetch domain name of site
    soup = BeautifulSoup(html, 'html.parser')
  
    for link in soup.find_all('a'):
      if link.get('href') != None and 'about' in link.get('href').lower() and domain in link.get('href').lower():
        return link.get('href')
  except:
    return None


def get_static_text_content(url):
  """ scrap static content form url and preprocess it """

  content = []
  
  try:
    with Timeout(30):
      res = requests.get(url, headers=headers, verify=False, timeout=10)
      content.extend(processdata.preprocess(text_from_html(res.text)))
      if len(content) > 0 and content[0] == "invalidcontentfound": return content

      abt_url = get_about_url(res.text, url)

      if abt_url != None:
        res = requests.get(abt_url, headers=headers, verify=False, timeout=10)
        content.extend(processdata.preprocess(text_from_html(res.text)))
      return content
    
  except:
    return content
  return content


def get_dynamic_text_content(url):
  """ scrap dynamic content form url and preprocess it """
  
  content = []
  try:
    browser.get(url)
    content.extend(processdata.preprocess(text_from_html(browser.page_source)))
    if len(content) > 0 and content[0] == "invalidcontentfound": return content
    abt_url = get_about_url(browser.page_source, url)
   
    if abt_url != None:
      browser.get(abt_url)
      content.extend(processdata.preprocess(text_from_html(browser.page_source)))
    return content
  except:
    return content


def get_scrapped_text(url, dynamic):
  """ scrap text content from url """

  content = get_static_text_content(url) 
  if len(content) > 0 and content[0] == "invalidcontentfound": return []
  dy_content = []
  if (len(content) < SUFFICIENT and dynamic): dy_content = get_dynamic_text_content(url)
  if len(dy_content) > 0 and dy_content[0] == "invalidcontentfound": dy_content =  []
  if len(content) >= len(dy_content): return content
  else: return dy_content


def get_url_and_content(url, dynamic=True):
  """ return dictionary object with url, and scrapped_content """

  final_url = url
  content = []
  
  if url.startswith('http'):
    content = get_scrapped_text(url, dynamic)
  else:
    content = get_scrapped_text('https://'+url, dynamic)
    final_url = 'https://'+url
    if len(content) < MINIMUM:
      content = get_scrapped_text('http://'+url, dynamic)
      final_url = 'http://'+url
  
  return {'url': final_url, 'content': ' '.join(content)}


def get_text_content(url, dynamic=True):
  """ params -: url -: as a string with or without http/https
                Note it will find suitable protocol b/w http and https automatically if doesn't include in url
                dynamic -: boolean variable to decide whether to scrap dynamic content or not

                return -: string consist text content from url 
                          or 
                          raise exception when _i) either url is invalid/inactive
                                                ii) site doen't have english content
                                                iii) failed to scrap significant amount of content 
                                                iv) sites take too long to respond """  


  content =  get_url_and_content(url, dynamic)['content']
  if len(content.split()) >= MINIMUM: return content
  else: raise


