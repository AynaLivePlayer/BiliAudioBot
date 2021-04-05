import pyncm

def patchPyncm():
    pyncm.GetCurrentSession().headers['X-Real-IP'] = '118.88.88.88'