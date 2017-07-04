#! coding:utf8

# pylint: disable=C0111,C0103,C0301

import urllib
import urllib2
import os
import base64
from Crypto.Cipher import AES

def aes_encrypt(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(sec_key, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsa_encrypt(text, pub_key, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pub_key, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secret_key(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


def encrypt_request(url, data):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pub_key = '010001'

    sec_key = create_secret_key(16)
    enc_text = aes_encrypt(aes_encrypt(data, nonce), sec_key)
    enc_sec_key = rsa_encrypt(sec_key, pub_key, modulus)

    param_dict = {
        'params': enc_text,
        'encSecKey': enc_sec_key
    }
    param_data = urllib.urlencode(param_dict)
    return urllib2.urlopen(url, param_data).read().decode('utf-8')
