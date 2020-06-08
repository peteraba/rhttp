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

lib.sha512_encode.argtypes = (c_void_p, )
lib.sha512_encode.restype = c_void_p

lib.sha3_512_encode.argtypes = (c_void_p, )
lib.sha3_512_encode.restype = c_void_p

lib.get.argtypes = (c_void_p, )
lib.get.restype = c_void_p

lib.post_xml.argtypes = (c_void_p, c_void_p, )
lib.post_xml.restype = c_void_p

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
    ptr1 = lib.sha512_encode(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

def sha3_512(text, expected):
    ptr1 = lib.sha3_512_encode(text.encode('utf-8'))
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

def postXml(url, body):
    ptr1 = lib.post_xml(url.encode('utf-8'), body.encode('utf-8'))
    try:
        response = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return response
    finally:
        lib.free_string(ptr1)

tokenUrl = "https://api-test.onlineszamla.nav.gov.hu/invoiceService/tokenExchange"
tokenPayload = """<?xml version="1.0" encoding="UTF-8"?>
<TokenExchangeRequest xmlns="http://schemas.nav.gov.hu/OSA/2.0/api">
	<header>
		<requestId>RID896801578348</requestId>
		<timestamp>2019-09-11T10:55:31.440Z</timestamp>
		<requestVersion>2.0</requestVersion>
		<headerVersion>1.0</headerVersion>
	</header>
	<user>
		<login>lwilsmn0uqdxe6u</login>
		<passwordHash>2F43840A882CFDB7DB0FEC07D419D030D864B47B6B541DC280EF81B937B7A176E33C052B0D26638CC18A7A2C08D8D311733078A774BF43F6CA57FE8CD74DC28E</passwordHash>
		<taxNumber>11111111</taxNumber>
		<requestSignature>B4B5E0F197BFFD3DF69BCC98D3BE775F65FD5445EEF95C9D6B6C59425F2B81C4F6DA1FD563B0C7E7D98AF1E1725E5C63C2803B5D3A93D1C02ED354AC92F2CC94</requestSignature>
		<!--<signKey>ac-ac3a-7f661bff7d342N43CYX4U9FG</signKey>-->
	</user>
	<software>
		<softwareId>123456789123456789</softwareId>
		<softwareName>string</softwareName>
		<softwareOperation>LOCAL_SOFTWARE</softwareOperation>
		<softwareMainVersion>string</softwareMainVersion>
		<softwareDevName>string</softwareDevName>
		<softwareDevContact>string</softwareDevContact>
		<softwareDevCountryCode>HU</softwareDevCountryCode>
		<softwareDevTaxNumber>string</softwareDevTaxNumber>
	</software>
</TokenExchangeRequest>"""

print(base64("any carnal pleasure."))
print(sha512("mysecret", "7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c"))
print(sha3_512("mysecret", "ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81"))
print(get("https://api-test.onlineszamla.nav.gov.hu/"))
print(postXml(tokenUrl, tokenPayload))
