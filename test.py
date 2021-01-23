#!/usr/bin/env python3

import argparse, ctypes, os
from ctypes import c_void_p, c_int32, c_float, c_double, POINTER, byref

parser = argparse.ArgumentParser()
parser.add_argument("--dll", help="full path of .dll file")
args = parser.parse_args()

dll = os.path.abspath(args.dll)
lib = ctypes.cdll.LoadLibrary(dll)

# Helpers
def compare(a, b):
    if a == b:
        return True
    
    return (False, a, b)

# Definitions
lib.free_string.argtypes = (c_void_p, )

lib.base64_encode.argtypes = (c_void_p, )
lib.base64_encode.restype = c_void_p

lib.base64_decode.argtypes = (c_void_p, )
lib.base64_decode.restype = c_void_p

lib.zip_base64_encode.argtypes = (c_void_p, )
lib.zip_base64_encode.restype = c_void_p

lib.zip_base64_decode.argtypes = (c_void_p, )
lib.zip_base64_decode.restype = c_void_p

lib.sha512_hash.argtypes = (c_void_p, )
lib.sha512_hash.restype = c_void_p

lib.sha3_512_hash.argtypes = (c_void_p, )
lib.sha3_512_hash.restype = c_void_p

lib.aes_encrypt.argtypes = (c_void_p, c_void_p, c_int32, POINTER(c_int32), )
lib.aes_encrypt.restype = c_void_p

lib.aes_decrypt.argtypes = (c_void_p, c_void_p, c_int32, POINTER(c_int32), )
lib.aes_decrypt.restype = c_void_p

lib.get_plain.argtypes = (c_void_p, POINTER(c_int32), )
lib.get_plain.restype = c_void_p

lib.post_xml.argtypes = (c_void_p, c_void_p, POINTER(c_int32), )
lib.post_xml.restype = c_void_p

lib.post_json.argtypes = (c_void_p, c_void_p, POINTER(c_int32), )
lib.post_json.restype = c_void_p

def base64_encode(text):
    res = ""

    ptr1 = lib.base64_encode(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def base64_decode(text):
    res = ""

    ptr1 = lib.base64_decode(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def zip_base64_encode(text):
    res = ""

    ptr1 = lib.zip_base64_encode(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def zip_base64_decode(text):
    res = ""

    ptr1 = lib.zip_base64_decode(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def sha512(text):
    res = ""

    ptr1 = lib.sha512_hash(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def sha3_512(text):
    res = ""

    ptr1 = lib.sha3_512_hash(text.encode('utf-8'))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(ptr1)

    return res

def aes_encrypt(plaintext, key, flags):
    err_code = 0
    res = ""

    c = c_int32(0)
    ptr1 = lib.aes_encrypt(plaintext.encode('utf-8'), key.encode('utf-8'), flags, c)

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        err_code = c.value
    finally:
        lib.free_string(ptr1)

    return (res, err_code)

def aes_decrypt(ciphertext, key, flags):
    err_code = 0
    res = ""

    c = c_int32(0)
    ptr1 = lib.aes_decrypt(ciphertext.encode('utf-8'), key.encode('utf-8'), flags, c)

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        err_code = c.value
    finally:
        lib.free_string(ptr1)

    return (res, err_code)

def get_plain(url):
    code = 0
    res = ""

    c = c_int32(0)
    ptr1 = lib.get_plain(url.encode('utf-8'), byref(c))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        code = c.value
    finally:
        lib.free_string(ptr1)

    return (code, res)

def post_xml(url, body):
    code = 0
    res = ""

    c = c_int32(0)
    ptr1 = lib.post_xml(url.encode('utf-8'), body.encode('utf-8'), byref(c))

    try:
        res = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        code = c.value
    finally:
        lib.free_string(ptr1)

    return (code, res)

def post_json(url, body):
    code = 0
    content = ""

    c = c_int32(0)
    ptr1 = lib.post_json(url.encode('utf-8'), body.encode('utf-8'), byref(c))

    try:
        content = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        code = c.value
    finally:
        lib.free_string(ptr1)

    return (code, content)

lorem_ipsum_hu = 'Vényítés hehez egyébként bodta, hogy a redés abban a pánságban havóval vátszik, amikor végre tapolyhoz irdíti majd a tűnőségöket.'
print(compare(lorem_ipsum_hu, base64_decode(base64_encode(lorem_ipsum_hu))))

# print(compare(sha512("mysecret"), "7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c"))

print(compare(sha512("Eco8901Comp"), "bf254c9966f54d8a662417c78895aa9f197809308ac65e034361557ab3b08cfe931ee4e64c77af42b1e5c095d69e6a8f79dff1ab832bc0732faea4902aa187d8"))

print(compare(sha3_512("mysecret"), "ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81"))

# input:  plain   -> 0000 0000
# output: base64  -> 0000 1000
# key:    hex     -> 0001 0000
print(compare(aes_encrypt("hello", "000102030405060708090a0b0c0d0e0f", 0x18), ('XYdJ4q91MbK/ZmHp5drwEg==', 0)))

# input:  base64  -> 0000 0010
# output: plain   -> 0000 0000
# key:    hex     -> 0001 0000
print(compare(aes_decrypt("XYdJ4q91MbK/ZmHp5drwEg==", "000102030405060708090a0b0c0d0e0f", 0x12), ('hello', 0)))

# print(get_plain("https://reqbin.com/echo"))
# print(post_xml("https://reqbin.com/echo/post/xml", '<?xml version="1.0" ?></xml>'))
# print(post_json("https://reqbin.com/echo/post/json", '{}'))

text = 'abc' * 10000
compressed = zip_base64_encode(text)
print(len(text), len(compressed))
print(compressed)
print(compare(text, zip_base64_decode(compressed)))

# data = "H4sIAAAAAAAAAM1YS2+jOhTe31+Buk5iIH1MKwaJJDRFeQpopGbnG5zGEq+LIUqWs+x6pFncv5M/dm1IeEwxSUd3NM0qnPOdY3+fz7ENiuFvA7xCAxhDYee5Pvl6tYnj8AEAstogD5KOD7ed12Db2SRgZmlA7ojAoegr9S+B/hScJZgm3t8oUq0l6Mr3oijeAVGWpC+A/hVlBVRRlUiDkISNj1SZhrRFqS0VAYWzEjOB2M8sZWthKVufEHSqntRLkjB0MYoMfx28d1cgNtyVJ16LjeEuhHuazlEl8V6U5C4lUTLyI7cw7gcOZa+A018+eBUkfrxPQdfXCig91lMAF3LIuU6hh9SJNnzRTGE+s2xNWJp2p8iT+ptTaI4TIUIaWBDshS46iysYRxnHp+cj5aiBcx4ZBiSGbgqUpO4XBZQMZ8bE8V7tPQ+0uW7ZdEj22BwBHQfHOPChe2Q1QDHErjp4nmoLwzx8GwrPdl8T5PYtFZOH5isGLpCsWCQurIDUl72ySkgceI1dcYJ8uCvE++6NfH2+K6jglw2RTyUtyiu2YIYws+2n2fRKGGujwzfrUZ9Obc20D98Fa3n4sdDtkb7U7WKIhno+QT5lPcu3f6See4cfTEdzcnibvhjC4V9b6Irtrvwbi/rsMhQQTlEfD4Km+ZwwfXrUvAbRXrWMyXxsPBr6ID+Lcl9jhgFy8RZFe96JVvHzCi+KkL861cgjI1iy1Aeh3WoD/VdksrySAirPnA0buesedl3svxq+g1cwDiJ1DV2C6NLU+erT0Gb2kB9PULwJHLWvWU+0NCs2Dk1INtoqrf+6GfDcjeprYYhgBH16GZjTajdz2UuOmgJqqJDc+f4ecRp0jH1UV5dUPJ70zHXc2uhalZ74cH0XsvqnHVZoEUcJysLrvPxcA0RWEQ5Zu9KWfhu/6MOWIMk3wuFtoVuCJkxmPaE3no1GWfYyvj7rPwmk60T3FUon/18PTXwcz9YTBEkS0WUy9L6ugKqRHziP2EXvThKzkOzxDJy20E8RzMJXR/NY0RGL7U54jVHT7Y3hF+za5se03lUx06tkaQ4dRgEh2Xil4dLJ8t2/kDKXoBHB2YEv1CQD/nIfyH+4D8b6gnZCa2Etx/ZDr3UjisO2MWzR9jAnnQcqnvBot0bW8kFrzU2jZS8+Z2vc3n20NaoRn7w10sn+763RnPX3tEZ+sNQcH6eTxUo8D9bdOOjLVuo5Rz17u8wXYHtG/BK8pIRK354qwWXfB/IwHRtS1crM3ljOMj2pkSZjnzKaLwnvqdU4Ls1QkKr38RlxZpsnerf4uef4MQRUvoYooPQtR/0PR5RcPNkRAAA="
# print(zip_base64_decode(data))
