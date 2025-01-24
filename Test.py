from hashlib import sha256

from Blockchain.Backend.Util.util import decode_base58, hash256


private_key =  '76106471728427465796187510860355568160254207807680397589831754374945066693457'
public_address =  "1LYgXwYXw16GJXgDwHV7aCNijnQWYEdc1C"

print(decode_base58(public_address))
print(hash256(private_key.encode()))

"hash160(publicKey) == public_address"