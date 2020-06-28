```
If you call a method that will return a string, you will need to call the free_string method to stop this .dll from leaking memory!
```

## Installation

### Build 32-bit .dll

```
cargo build --target=i686-pc-windows-msvc --release
```

Output file: `.\target\i686-pc-windows-msvc\release\rhttp.dll`


### Build 64-bit .dll

```
cargo build --target=x86_64-pc-windows-msvc --release
```

Output file: `.\target\x86_64-pc-windows-msvc\release\rhttp.dll`

## Test via python 3

```
> python3 .\test.py --dll .\target\x86_64-pc-windows-msvc\release\rhttp.dll
True
True
True
OK
True
True
```

## Methods

### Base64 encode and decode

```rust
fn base64_decode(s: *const c_char) -> *mut c_char {}
fn base64_encode(s: *const c_char) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.sha512_hash.argtypes = (c_void_p, )
lib.sha512_hash.restype = c_void_p

def sha512(text, expected):
    ptr1 = lib.sha512_hash(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

print(sha512("mysecret", "7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c"))
```

### Hashing via SHA-512

```rust
fn sha512_hash(s: *const c_char) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.sha512_hash.argtypes = (c_void_p, )
lib.sha512_hash.restype = c_void_p

def sha512(text, expected):
    ptr1 = lib.sha512_hash(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

print(sha512("mysecret", "7b6f7690ae2a5ecdf66b3db2adf91340a680da1ab82561796b8504db942476967369814aa35050dd86838848c1ba703450f2f5e21b0a8e4cff690b855ae5bd8c"))
```

### Hashing via SHA3-512

```rust
fn sha3_512_hash(s: *const c_char) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.sha3_512_hash.argtypes = (c_void_p, )
lib.sha3_512_hash.restype = c_void_p

def sha3_512(text, expected):
    ptr1 = lib.sha3_512_hash(text.encode('utf-8'))
    try:
        hashed = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')
        if hashed == expected:
            return True

        return (hashed == expected, hashed, expected)
    finally:
        lib.free_string(ptr1)

print(sha3_512("mysecret", "ef846feafed891792553756277b48e90784eca281f683920551f36b359833b10aab4897765050e398232e3f213fe49c7c50271f339d4797c25dc58c3d7f33f81"))
```

### AES encrypt and decrypt

`aes_encrypt` and `aes_decrypt` are used to encrypt and decrypt messages via using [AES-128](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) block cipher in [ECB mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)) and with [PKCS#7 padding](https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS#5_and_PKCS#7).

Both method works primarily on byte arrays which you can provide as `plain text`, `hexadecimal representation` and `base64 encoding`. These can be configured by setting the plans as designed:

Flags can be provided as a 32-bit integer (for compatibility reasons), which then will be converted into an unsigned integer. These flags can be combined, but some combinations will be ignored:
- 0x01 - Input is provided as `hexadecimal representation`
- 0x02 - Input is provided using `base64 encoding`
- 0x04 - Output should be returned in a `hexadecimal representation`
- 0x08 - Output should be returned using `base64 encoding`
- 0x10 - Key is provided as `hexadecimal representation`
- 0x20 - Key is provided using `base64 encoding`

```rust
fn aes_encrypt(c_plaintext: *const c_char, c_key: *const c_char, flags: i32) -> *mut c_char {}

fn aes_decrypt(c_ciphertext: *const c_char, c_key: *const c_char, flags: i32) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.aes_encrypt.argtypes = (c_void_p, c_void_p, c_int32, )
lib.aes_encrypt.restype = c_void_p

lib.aes_decrypt.argtypes = (c_void_p, c_void_p, c_int32, )
lib.aes_decrypt.restype = c_void_p

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

print(aes_encrypt("hello", "000102030405060708090a0b0c0d0e0f", 0x18, 'XYdJ4q91MbK/ZmHp5drwEg=='))

print(aes_decrypt("XYdJ4q91MbK/ZmHp5drwEg==", "000102030405060708090a0b0c0d0e0f", 0x12, 'hello'))
```

### HTTP(s) GET

```rust
fn get(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {}
fn get_xml(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {}
fn get_json(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.get.argtypes = (c_void_p, POINTER(c_int32), )
lib.get.restype = c_void_p

def get(url):
    c = c_int32(0)
    ptr1 = lib.get(url.encode('utf-8'), byref(c))
    try:
        content = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return (c.value, content)
    finally:
        lib.free_string(ptr1)

print(get("https://api-test.onlineszamla.nav.gov.hu/"))
```

`get_plain`, `get_xml`, `get_json` only differ in the headers sent along with the request.

### HTTP(s) POST

```rust
fn post_plain(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.post_xml.argtypes = (c_void_p, c_void_p, POINTER(c_int32), )
lib.post_xml.restype = c_void_p

def post_xml(url, body):
    c = c_int32(0)
    ptr1 = lib.post_xml(url.encode('utf-8'), body.encode('utf-8'), byref(c))
    try:
        content = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return (c.value, content)
    finally:
        lib.free_string(ptr1)

print(post_xml("https://example.com/tokenExchange", 'field1=value1&field2=value2'))
```

### HTTP(s) POST with XML headers

```rust
fn post_xml(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.post_xml.argtypes = (c_void_p, c_void_p, POINTER(c_int32), )
lib.post_xml.restype = c_void_p

def post_xml(url, body):
    c = c_int32(0)
    ptr1 = lib.post_xml(url.encode('utf-8'), body.encode('utf-8'), byref(c))
    try:
        content = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return (c.value, content)
    finally:
        lib.free_string(ptr1)

print(post_xml("https://example.com/xmlEndpoint", '<?xml version="1.0" ?></xml>'))
```


### HTTP(s) POST with JSON headers

```rust
fn post_json(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {}
```

Correct usage in python:

```python3
lib.post_json.argtypes = (c_void_p, c_void_p, POINTER(c_int32), )
lib.post_json.restype = c_void_p

def post_json(url, body):
    c = c_int32(0)
    ptr1 = lib.post_json(url.encode('utf-8'), body.encode('utf-8'), byref(c))
    try:
        content = ctypes.cast(ptr1, ctypes.c_char_p).value.decode('utf-8')

        return (c.value, content)
    finally:
        lib.free_string(ptr1)

print(post_json("https://example.com/jsonEndpoint", '{}'))
```
