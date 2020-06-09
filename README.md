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

### Hashing via SHA-512

```rust
fn sha512_hash(s: *const c_char) -> *mut c_char {}
```

### Hashing via SHA3-512

```rust
fn sha3_512_hash(s: *const c_char) -> *mut c_char {}
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

### HTTP(s) GET

```rust
fn get(c_url: *const c_char) -> *mut c_char
```

### HTTP(s) POST with XML headers

```rust
fn post_xml(c_url: *const c_char, c_body: *const c_char) -> *mut c_char
```
