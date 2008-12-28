from google.appengine.api import urlfetch
import urllib
import re

tb_ping_regex1 = re.compile('trackback:ping="(.*?)"')
tb_ping_regex2 = re.compile('href="(http://[^"\s]+trackback[^"\s])"')

def autodiscover(link_url):
    try:
        result = urlfetch.fetch(link_url)
        if result.status_code == 200:
            m = tb_ping_regex1.search(result.content)
            if m:
                return m.group(1)
            m = tb_ping_regex2.search(result.content)
            if m:
                return m.group(1)
    except:
        pass
    return None

class TrackBack(object):
    def __init__(self, title=None, excerpt=None, url=None, blog_name=None):
        self.params = urllib.urlencode({
            'title': title, 
            'excerpt': excerpt, 
            'url': url, 
            'blog_name': blog_name})
        self.headers = ({"Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "micolog-cxu/0.1.0 GAE"})

    def trackback(self, tb_url):
        # Only execute if a trackback url has been defined.
        if tb_url:
            try:
                result = urlfetch.fetch(url=tb_url,
                    payload=self.params,
                    method=urlfetch.POST,
                    headers=self.headers)
                return result.content
            except:
                pass
        return ''

    def ping(self, link_url):
        tb_url = autodiscover(link_url)
        return self.trackback(tb_url)

