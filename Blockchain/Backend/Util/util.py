import sys
from math import log
from Crypto.Hash import RIPEMD160
from hashlib import sha256
sys.path.append("C:/Users/Ary/dev/PyBlockChain")
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(data):
    return sha256(sha256(data).digest()).digest()

def hash160(s): # fixed function
    ripe = RIPEMD160.new()
    ripe.update(s)
    return ripe.digest()


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
    '''String turns into a Base 58 encoding'''
    num = 0

    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder="big")
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"bad Address {checksum} {hash256(combined[:-4][:4])}")

    return combined[1:-4]

def encode_varint(i):
    """encodes an integer as a varint"""
    if i < 0xFD:
        return bytes([i])
    elif i < 0x10000:
        return b"\xfd" + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b"\xfe" + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b"\xff" + int_to_little_endian(i, 8)
    else:
        raise ValueError("integer too large: {}".format(i))
    
def merkle_parent_level(hashes):
    '''Takes a list of hashes and returns a list that is half the length'''
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_level = []

    for i in range(0, len(hashes), 2):
        parent = hash256(hashes[i] + hashes[i+1])
        parent_level.append(parent)

    return parent_level

def merkle_root(hashes):
    '''Takes a list of hashes and returns the root of the merkle tree'''
    current_level = hashes

    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    return current_level[0]