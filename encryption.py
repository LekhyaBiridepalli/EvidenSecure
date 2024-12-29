# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes
# import base64

# # AES Encryption
# def encrypt_aes(data, key):
#     """Encrypt data using AES encryption."""
#     cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
#     ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
#     iv = base64.b64encode(cipher.iv).decode('utf-8')
#     ct = base64.b64encode(ct_bytes).decode('utf-8')
#     return iv + ct  # Return both IV and ciphertext concatenated

# # AES Decryption
# def decrypt_aes(data, key):
#     """Decrypt data using AES encryption."""
#     iv = base64.b64decode(data[:24])  # First 24 characters are the IV
#     ct = base64.b64decode(data[24:])  # Rest is the ciphertext
#     cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
#     pt = unpad(cipher.decrypt(ct), AES.block_size)
#     return pt.decode('utf-8')
import base64

# Dummy AES-like encryption function using base64 encoding
def encrypt_aes(plain_text, secret_key):
    """Encrypt the text by base64 encoding (for testing)"""
    # In a real scenario, you would use AES encryption here
    encoded_text = base64.b64encode(plain_text.encode('utf-8')).decode('utf-8')
    return encoded_text

# Dummy AES-like decryption function using base64 decoding
def decrypt_aes(encrypted_text, secret_key):
    """Decrypt the text by base64 decoding (for testing)"""
    # In a real scenario, you would use AES decryption here
    decoded_text = base64.b64decode(encrypted_text.encode('utf-8')).decode('utf-8')
    return decoded_text
