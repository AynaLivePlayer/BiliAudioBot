import threading
from queue import Queue

import requests,traceback


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
                return requests.get(url, timeout=5, **kwargs)
            except:
                traceback.print_exc()
                trial += 1
        return None

    def post(self,url,**kwargs):
        trial = 0
        while trial < self.maxTrial:
            try:
                return requests.post(url, timeout=5, **kwargs)
            except:
                traceback.print_exc()
                trial += 1
        return None


class ThreadingHttpClient:
    def __init__(self,maxTrial = 5):
        self.maxTrial = maxTrial

    def _req(self, func, url, q: Queue, *args, **kwargs):
        trial = 0
        while trial < self.maxTrial:
            try:
                return q.put(func(url, timeout=5, *args, **kwargs))
            except:
                traceback.print_exc()
                trial += 1
        q.put(None)

    def get(self,url,**kwargs):
        q = Queue()
        thread = threading.Thread(target=self._req,args=(requests.get,url,q,),kwargs=kwargs)
        thread.start()
        thread.join()
        return q.get()

    def post(self,url,**kwargs):
        q = Queue()
        thread = threading.Thread(target=self._req, args=(requests.post, url, q,), kwargs=kwargs)
        thread.start()
        thread.join()
        return q.get()