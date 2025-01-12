# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# import os
# from base64 import b64encode, b64decode

# # Key and IV should ideally be stored securely, not hard-coded.
# key = os.urandom(32)  # 256-bit key for AES
# iv = os.urandom(16)   # 128-bit IV

# def encrypt_data(data):
#     # Pad the data to make it a multiple of block size
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_data = padder.update(data.encode()) + padder.finalize()

#     # Encrypt the padded data
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

#     # Return encrypted data in base64 encoding for storage in MongoDB
#     return b64encode(encrypted_data).decode()

# def decrypt_data(encrypted_data):
#     # Decode the base64 encoded encrypted data
#     encrypted_data = b64decode(encrypted_data)

#     # Decrypt the data
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

#     # Unpad the decrypted data
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

#     # Return decrypted data as a string
#     return unpadded_data.decode()



from datetime import datetime
from cryptography.fernet import Fernet
from gridfs import GridFS
from pymongo import MongoClient
from .db import *

fs = GridFS(db)

# Generate encryption key (should be stored securely in production)
key = Fernet.generate_key()  # In production, store this securely
cipher_suite = Fernet(key)

# Encrypt text data
def encrypt_data(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()

# Encrypt file data
def encrypt_file(file_data: bytes) -> bytes:
    return cipher_suite.encrypt(file_data)

# Save encrypted evidence and files to MongoDB and GridFS
def save_encrypted_evidence(case_id, evidence_type, evidence_description, collected_by, file_data, file_name, file_type):
    # Save the encrypted file to GridFS
    file_id = fs.put(file_data, filename=file_name, content_type=file_type)

    # Save the metadata (encrypted data) in the 'evidence' collection
    evidence = {
        "case_id": case_id,
        "evidence_type": evidence_type,  # Encrypted
        "evidence_description": evidence_description,  # Encrypted
        "collected_by": collected_by,  # Encrypted
        "files": [
            {
                "file_id": file_id,
                "file_type": file_type,
                "file_name": file_name,
                "file_size": len(file_data)  # Store file size
            }
        ],
        "upload_date": datetime.now()
    }

    # Insert evidence document into MongoDB collection
    db.evidence.insert_one(evidence)


