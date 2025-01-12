
import hashlib
import json
import logging
import base64
import os
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.contrib.auth.hashers import make_password
import re


from pymongo import MongoClient
import gridfs
from bson import ObjectId

# Custom imports
from .db import *  # Import the MongoDB connection
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def get_cipher():
    key = settings.ENCRYPTION_KEY  # Already in bytes
    iv = settings.ENCRYPTION_IV  # Already in bytes
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher

def encrypt_content(plain_text):
    cipher = get_cipher()
    encryptor = cipher.encryptor()
    padded_data = plain_text + (16 - len(plain_text) % 16) * ' '
    encrypted_data = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')

def encrypt_file(file_data):
    # Encrypt the file content using the same key and IV from settings
    cipher = Cipher(algorithms.AES(settings.ENCRYPTION_KEY), modes.CBC(settings.ENCRYPTION_IV), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the file data
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt_content(encrypted_text):
    cipher = get_cipher()
    decryptor = cipher.decryptor()
    encrypted_data = base64.b64decode(encrypted_text)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode('utf-8').rstrip()  # Remove padding

def decrypt_file(encrypted_file_data):
    cipher = Cipher(algorithms.AES(settings.ENCRYPTION_KEY), modes.CBC(settings.ENCRYPTION_IV), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the file data
    decrypted_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data