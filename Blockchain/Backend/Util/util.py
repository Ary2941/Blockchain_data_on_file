import sys
from math import log
from Crypto.Hash import RIPEMD160
from hashlib import sha256
sys.path.append("C:/Users/Ary/dev/PyBlockChain")
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(data):
    return sha256(sha256(data).digest()).digest()

def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

def int_to_little_endian(n,length):
    '''int to little endian, used in coinbase transaction
    return little endian byte sequence of length given
    '''
    return n.to_bytes(length, 'little')

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n,256)) + 1

def decode_base58(s):
    num = 0

    for c in s:
        print(f"c: {c} {c in BASE58_ALPHABET}")
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder="big")
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"bad Address {checksum} {hash256(combined[:-4])[:4]}")

    return combined[1:-4]
