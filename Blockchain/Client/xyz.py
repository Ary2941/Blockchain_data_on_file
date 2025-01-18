import hashlib

# Função auxiliar hash256
def hash256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# Função para gerar o endereço a partir da chave privada
def private_key_to_address(private_key):
    # Supondo que o private_key seja um inteiro em forma de string
    private_key_bytes = int(private_key).to_bytes(32, byteorder="big")

    # Passo 1: Geração da chave pública (poderia usar ECDSA ou outro algoritmo de assinatura)
    public_key = private_key_to_public_key(private_key_bytes)

    # Passo 2: Gerar o endereço
    address = public_key_to_base58(public_key)

    return address

# Função para converter a chave pública para um endereço Base58 (simplificado)
def public_key_to_base58(public_key):
    # Passo 1: Prefixo (ex: 0x00 para Bitcoin)
    prefix = b'\x00'

    # Passo 2: Gerar o hash160 (RIPEMD160 após SHA256)
    hash160 = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()

    # Passo 3: Concatenar o prefixo com o hash160
    combined = prefix + hash160

    # Passo 4: Calcular o checksum (hash256 dos primeiros 21 bytes)
    checksum = hash256(combined)[:4]

    # Passo 5: Concatenar o checksum e gerar a string Base58
    address_bytes = combined + checksum
    address = base58_encode(address_bytes)
    
    return address

# Função para codificar em Base58
def base58_encode(data):
    BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(data, byteorder="big")
    base58 = ""
    
    while num > 0:
        num, rem = divmod(num, 58)
        base58 = BASE58_ALPHABET[rem] + base58
    
    return base58

# Exemplo de uso
private_key = '104247066611994639534832141156469009640440611541825514866670397177959661446949'
miner_address = private_key_to_address(private_key)
print(miner_address)
