import pyncm

def patchPyncm():
    pyncm.GetCurrentSession().headers['X-Real-IP'] = '118.88.88.88'

def filterTclSpecialCharacter(chars):
    return "".join(map(lambda s: s if 0<= ord(s) <= 65535 else "?",chars))
