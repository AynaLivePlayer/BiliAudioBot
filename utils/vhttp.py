import requests



def httpGet(url, maxReconn=5, **kwargs):
    trial = 0
    while trial < maxReconn:
        try:
            return requests.get(url, timeout=5, **kwargs)
        except:
            trial += 1
            continue
    return None

def httpPost(url, maxReconn=5,**kwargs):
    trial = 0
    while trial < maxReconn:
        try:
            return requests.post(url, timeout=5, **kwargs)
        except:
            trial += 1
            continue
    return None


class HttpClient:
    def __init__(self,maxTrial = 5):
        self.maxTrial = maxTrial

    def get(self,url,**kwargs):
        trial = 0
        while trial < self.maxTrial:
            try:
                return requests.get(url, timeout=5, **kwargs).content
            except:
                trial += 1
        return b''

    def post(self,url,**kwargs):
        trial = 0
        while trial < self.maxTrial:
            try:
                return requests.post(url, timeout=5, **kwargs).content
            except:
                trial += 1
        return b''