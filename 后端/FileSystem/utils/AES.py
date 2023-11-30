import json
import os

from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms

from utils.JWT import get_aes_key, get_aes_iv
#https://www.jianshu.com/p/5b38b4187b54
from flask import session


def add_to_16(text):#密钥填充至要求长度
    while len(text) % 16 != 0:
        text += '\0'
    return (text)

def pad(uppadded_data):
    if not isinstance(uppadded_data, bytes):
        uppadded_data = uppadded_data.encode()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(uppadded_data) + padder.finalize()
    return padded_data

def unpad(padded_data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        uppadded_data = unpadder.update(padded_data) + unpadder.finalize()
    except ValueError:
        raise Exception('无效的加密信息!')
    else:
        return uppadded_data

def encrypt(data):
    if type(data)==bytes:
        data=str(data,encoding = "utf-8")
    key = bytes.fromhex(get_aes_key())
    iv = bytes.fromhex(get_aes_iv())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    return data.hex()
def download_encrypt(data):
    key = bytes.fromhex(get_aes_key())
    iv = bytes.fromhex(get_aes_iv())
    cipher = AES.new(key, AES.MODE_CBC, iv)

    uppadded_data=data
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(uppadded_data) + padder.finalize()

    data = cipher.encrypt(padded_data)
    print(data[:32].hex())
    return data.hex()

def decrypt(data):
    bs = AES.block_size
    if len(data) <= bs:
        return (data)
    key = bytes.fromhex(get_aes_key())
    iv = bytes.fromhex(get_aes_iv())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(bytes.fromhex(data.decode("utf-8"))))
    return json.loads(data.decode("utf-8"))

