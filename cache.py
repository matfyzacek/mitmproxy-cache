#you need to create folder named cache for this script to work
from mitmproxy import ctx
from mitmproxy import http
from os.path import exists
import threading
import hashlib,requests,pickle
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
class Counter:
    def __init__(self):
        self.num = 0
    def md5(self,stri):
        return str(hashlib.md5(bytes(stri,"UTF8")).hexdigest())
    def had(self,url):
        url=url
        if not "http://" in url or "https://" in url:
            return "http://"+url
        return url
    def remalgs(self,url):
        u = urlparse(url)
        query = parse_qs(u.query, keep_blank_values=True)
        query.pop('utm_source', None)
        query.pop('utm_medium', None)
        query.pop('utm_campaign', None)
        query.pop('utm_term', None)
        query.pop('utm_content', None)
        u = u._replace(query=urlencode(query, True))
        return str(urlunparse(u))
    def save(self,url,sc,cnt,hds):
        f=open("cache/"+self.md5(str(self.remalgs(url))),"wb")
        f.write(pickle.dumps({"status_code":sc,"content":cnt,"headers":hds}))
        f.close()
    def request(self,flow:http.HTTPFlow) -> None:
        if exists("cache/"+self.md5(str(flow.request.url))):
            f=open("cache/"+self.md5(self.remalgs(str(flow.request.url))),"rb")
            data=pickle.loads(f.read())
            f.close()
            flow.response = http.Response.make(data["status_code"], data["content"], data["headers"])
            ctx.log.info("####################loading from cache")
        else:
            return
    def response(self,flow):
            tbr=threading.Thread(target=self.save,args=(flow.request.url,flow.response.status_code,flow.response.content,dict(flow.response.headers)))
            tbr.start()
        
addons = [
    Counter()
]
