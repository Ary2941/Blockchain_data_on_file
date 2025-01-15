import hashlib

from Crypto.Hash import RIPEMD160
from hashlib import sha256

def hash256(s):
    """ Dois rounds de SHA256"""
    return hashlib.sha256(hashlib.sha256(str(s).encode()).digest()).digest()
def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()