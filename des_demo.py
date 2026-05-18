

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 8


# -------------------------------------------------
# FORMAT KEY
# DES requires exactly 8 bytes
# -------------------------------------------------

def format_key(key):

    key = key.encode()

    if len(key) < 8:
        key = key.ljust(8, b'0')

    return key[:8]


# -------------------------------------------------
# ECB ENCRYPTION
# -------------------------------------------------

def encrypt_ecb(plaintext, key):

    key = format_key(key)

    cipher = DES.new(key, DES.MODE_ECB)

    padded_text = pad(plaintext.encode(), BLOCK_SIZE)

    encrypted = cipher.encrypt(padded_text)

    return encrypted.hex()


# -------------------------------------------------
# ECB DECRYPTION
# -------------------------------------------------

def decrypt_ecb(ciphertext_hex, key):

    key = format_key(key)

    cipher = DES.new(key, DES.MODE_ECB)

    ciphertext = bytes.fromhex(ciphertext_hex)

    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted, BLOCK_SIZE).decode()


# -------------------------------------------------
# CBC ENCRYPTION
# -------------------------------------------------

def encrypt_cbc(plaintext, key):

    key = format_key(key)

    iv = get_random_bytes(8)

    cipher = DES.new(key, DES.MODE_CBC, iv)

    padded_text = pad(plaintext.encode(), BLOCK_SIZE)

    encrypted = cipher.encrypt(padded_text)

    return {
        "iv": iv.hex(),
        "ciphertext": encrypted.hex()
    }


# -------------------------------------------------
# CBC DECRYPTION
# -------------------------------------------------

def decrypt_cbc(ciphertext_hex, key, iv_hex):

    key = format_key(key)

    iv = bytes.fromhex(iv_hex)

    cipher = DES.new(key, DES.MODE_CBC, iv)

    ciphertext = bytes.fromhex(ciphertext_hex)

    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted, BLOCK_SIZE).decode()


# -------------------------------------------------
# MODE COMPARISON
# -------------------------------------------------

def compare_modes(plaintext, key):

    ecb_cipher = encrypt_ecb(plaintext, key)

    cbc_result = encrypt_cbc(plaintext, key)

    return {
        "ECB": ecb_cipher,
        "CBC_IV": cbc_result["iv"],
        "CBC_Ciphertext": cbc_result["ciphertext"]
    }


# -------------------------------------------------
# EDUCATIONAL PATTERN TEST
# -------------------------------------------------

def repeated_block_demo():

    text = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    key = "mykey123"

    result = compare_modes(text, key)

    return result


# -------------------------------------------------
# STANDALONE TEST
# -------------------------------------------------

if __name__ == "__main__":

    sample_text = "HELLO INFORMATION SECURITY"

    sample_key = "secure12"

    print("===== DES ECB vs CBC Demo =====")

    result = compare_modes(sample_text, sample_key)

    print("\nECB Ciphertext:")
    print(result["ECB"])

    print("\nCBC IV:")
    print(result["CBC_IV"])

    print("\nCBC Ciphertext:")
    print(result["CBC_Ciphertext"])

    print("\n===== Pattern Leakage Demo =====")

    demo = repeated_block_demo()

    print("\nECB:")
    print(demo["ECB"])

    print("\nCBC:")
    print(demo["CBC_Ciphertext"])