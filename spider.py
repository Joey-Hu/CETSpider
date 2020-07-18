import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote
 
 
def get_html(url):
    try:
        html = requests.get(url).text
    except Exception as e:
        print('web requests url error: {}\nlink: {}'.format(e, url))
    return html
 
 
class WebDownloader(object):
 
    def __init__(self, base_url):
        self.url = base_url
        self.links = set()
 
    def parse_html(self, verbose=False):
        html = get_html(self.url)
        soup = BeautifulSoup(html)
        for link in soup.findAll('a'):
            if link.has_attr('href'):
                href = str(link.get('href'))
                if href.startswith('/Learn/CET/CET6'):
                    self.links.add(href)
                    if verbose:
                        print(link.get('href'))

    def download(self):
        for link in self.links:
            link = str(link)
            if link.endswith('.pdf'):
                link = 'https://pan.uvooc.com' + link
                file_name = unquote(link.split('/')[-1]) 
                try:
                    r = requests.get(link)
                    with open(file_name, 'wb+') as f:
                        f.write(r.content)
                except Exception as e:
                    print('Downloading error:{}\nlink:{}'.format(e, link))

            if link.endswith('.mp3'):
                link = 'https://pan.uvooc.com' + link
                file_name = unquote(link.split('/')[-1])
                try:
                    r = requests.get(link, stream=True)
                    with open(file_name, 'wb+') as m:
                        m.write(r.content)
                except Exception as e:
                    print('Downloading error:{}\nlink:{}'.format(e, link))
 

url_list = ['2018年06月英语六级真题', '2018年12月英语六级真题', '2019年06月英语六级真题', '2019年12月英语六级真题']
for li in url_list:
    url = 'https://pan.uvooc.com/Learn/CET/CET6/' +'/' + quote(li)
    wd = WebDownloader(url)
    wd.parse_html()
    pprint(wd.links)
    wd.download()
