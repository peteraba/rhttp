#!/usr/bin/env python3

import argparse, ctypes, os
from ctypes import c_void_p, c_int32, c_float, c_double

parser = argparse.ArgumentParser()
parser.add_argument("--dll", help="full path of .dll file")
args = parser.parse_args()

dll = os.path.abspath(args.dll)
lib = ctypes.cdll.LoadLibrary(dll)

# Definitions
lib.free_string.argtypes = (c_void_p, )

lib.base64_encode.argtypes = (c_void_p, )
lib.base64_encode.restype = c_void_p

lib.base64_decode.argtypes = (c_void_p, )
lib.base64_decode.restype = c_void_p

lib.sha512_hash.argtypes = (c_void_p, )
lib.sha512_hash.restype = c_void_p

lib.sha3_512_hash.argtypes = (c_void_p, )
lib.sha3_512_hash.restype = c_void_p

lib.get.argtypes = (c_void_p, )
lib.get.restype = c_void_p

lib.post_xml.argtypes = (c_void_p, c_void_p, )
lib.post_xml.restype = c_void_p

lib.aes_encrypt.argtypes = (c_void_p, c_void_p, c_int32, )
lib.aes_encrypt.restype = c_void_p

lib.aes_decrypt.argtypes = (c_void_p, c_void_p, c_int32, )
lib.aes_decrypt.restype = c_void_p

def base64(text):
    ptr1 = lib.base64_encode(text.encode('utf-8'))
    try:
        encoded = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        ptr2 = lib.base64_decode(encoded.encode('utf-8'))
        try:
            decoded = ctypes.cast(ptr2, ctypes.c_char_p).value.decode('utf-8')
            if decoded == text:
                return True

            return (decoded == text, encoded, decoded)
        finally:
            lib.free_string(ptr2)
    finally:
        lib.free_string(ptr1)

def sha512(text, expected):
    ptr1 = lib.sha512_hash(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

def sha3_512(text, expected):
    ptr1 = lib.sha3_512_hash(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

def get(url):
    ptr1 = lib.get(url.encode('utf-8'))
    try:
        response = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return response
    finally:
        lib.free_string(ptr1)

def post_xml(url, body):
    ptr1 = lib.post_xml(url.encode('utf-8'), body.encode('utf-8'))
    try:
        response = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return response
    finally:
        lib.free_string(ptr1)

def aes_encrypt(plaintext, key, flags, expected):
    ptr1 = lib.aes_encrypt(plaintext.encode('utf-8'), key.encode('utf-8'), flags)
    try:
        response = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if response == expected:
            return True

        return response
    finally:
        lib.free_string(ptr1)

def aes_decrypt(ciphertext, key, flags, expected):
    ptr1 = lib.aes_decrypt(ciphertext.encode('utf-8'), key.encode('utf-8'), flags)
    try:
        response = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if response == expected:
            return True

        return response
    finally:
        lib.free_string(ptr1)

print(base64('Vényítés hehez egyébként bodta, hogy a redés abban a pánságban havóval vátszik, amikor végre tapolyhoz irdíti majd a tűnőségöket. A rémetleg robákban a kató főzés hompai által a zsintőnél pidő hűsítő birt olyan kamatokat logazott fel, amelyek súlyosan szaborázják a zsintő bormogtatos rozásait. Ennek megfelelően az ömlés hompai a kanyós felebelő manákat és kirderedéseket a hályogó talányozott pachok felé kozatosék. 1 csengyedemer húzatás, 2 feke lenemek, 1 pikkely trozás, nészer, 1 vice párom, 4 vice haság, 1 ratyi melelő.'))
print(sha512("mysecret", "7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c"))
print(sha3_512("mysecret", "ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81"))
print(get("https://api-test.onlineszamla.nav.gov.hu/"))

# input:  plain   -> 0000 0000
# output: base64  -> 0000 1000
# key:    hex     -> 0001 0000
print(aes_encrypt("hello", "000102030405060708090a0b0c0d0e0f", 0x18, 'XYdJ4q91MbK/ZmHp5drwEg=='))

# input:  base64  -> 0000 0010
# output: plain   -> 0000 0000
# key:    hex     -> 0001 0000
print(aes_decrypt("XYdJ4q91MbK/ZmHp5drwEg==", "000102030405060708090a0b0c0d0e0f", 0x12, 'hello'))