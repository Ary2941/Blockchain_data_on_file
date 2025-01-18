import hashlib
import base58

private_key_decimal = 104247066611994639534832141156469009640440611541825514866670397177959661446949
private_key_hex = hex(private_key_decimal)[2:]  # Remove o prefixo '0x'

print(f"Private Key: {private_key_decimal}")
print("Private Key (Hex):", private_key_hex)


from ecdsa import SigningKey, SECP256k1

def generate_public_key(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    verifying_key = signing_key.verifying_key
    return b'\x04' + verifying_key.to_string()  # Adiciona prefixo 0x04 para chave pública não compactada

public_key = generate_public_key(private_key_hex)
print("Public Key (Hex):", public_key.hex())

def public_key_to_address(public_key):
    # 1. SHA-256 e RIPEMD-160
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

    # 2. Adicionar prefixo de rede
    network_prefix = b'\x00'  # Bitcoin Mainnet
    hashed_pubkey = network_prefix + ripemd160_hash

    # 3. Calcular checksum
    checksum = hashlib.sha256(hashlib.sha256(hashed_pubkey).digest()).digest()[:4]

    # 4. Codificar em Base58
    address_bytes = hashed_pubkey + checksum
    return base58.b58encode(address_bytes).decode()

address = public_key_to_address(public_key)
print("Generated Bitcoin Address:", address)

