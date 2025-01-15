import sys
sys.path.append('/Users/Ary/dev/PyBlockChain')
import secrets
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import Sha256Point
from Blockchain.Backend.Util.util import hash160, hash256
class Account:
    def createKeys(self):

        """Secp256k1 Curve Generator Points"""
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        
        G  = Sha256Point(Gx, Gy) 
        
        privateKey = secrets.randbits(256)
        
        unCompressedPublicKey = privateKey * G
        
        Xpoint = unCompressedPublicKey.x.num
        Ypoint = unCompressedPublicKey.y.num
        ''' is y even or odd?'''
        if Ypoint % 2 == 0:
            compressedKey = b'\x02' + Xpoint.to_bytes(32, 'big')
        else:
            compressedKey = b'\x03' + Xpoint.to_bytes(32, 'big')

        hash160v = hash160(compressedKey)
        """prefix for Mainnet"""
        main_prefix = b'\x00'
        newAddr = main_prefix + hash160v
        ''' checksum'''
        checksum = hash256(newAddr)[::4]

        newAddr += checksum
        
        BASE58_ALPHABET = '1234566789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        
        count = 0
        for c in newAddr:
            if c == 0:
                count += 1 
            else:
                break

        num = int.from_bytes(newAddr, 'big')
        prefix = '1' * count

        result = ''

        while num > 0:
            num, mod = divmod(num,58)
            result = BASE58_ALPHABET[mod]+result
        
        PublicAddress = prefix + result

        print(f"private key {privateKey}")
        print(f"public key {PublicAddress}")

        #print(f"sh: {privateKey}")


if __name__ == '__main__':
    acct = Account()
    acct.createKeys()