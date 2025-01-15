from Blockchain.Backend.Util.util import hash256

class BlockHeader:
    def __init__(self, version, previousBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.previousBlockHash = previousBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.BlockHash = ''
    
    def mine(self):
        while (self.BlockHash[0:4]) != '0000':
            self.BlockHash = hash256((str(self.version) + self.previousBlockHash + self.merkleRoot + str(self.timestamp) + self.bits + str(self.nonce)).encode()).hex()
            self.nonce += 1
            print(f" Mining Started {self.nonce} {self.BlockHash[0:4]}", end = '\r')