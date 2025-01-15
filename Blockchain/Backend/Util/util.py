import hashlib

def hash256(s):
    """ Dois rounds de SHA256"""

    return hashlib.sha256(hashlib.sha256(str(s).encode()).digest()).digest()