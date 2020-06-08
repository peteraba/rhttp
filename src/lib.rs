#[macro_use] extern crate hex_literal;
extern crate base64;
extern crate libc;
extern crate sha2;
extern crate sha3;
extern crate reqwest;
extern crate aes_soft as aes;
extern crate block_modes;

//external crates
use aes::Aes128;
use block_modes::{Ecb};
use block_modes::block_padding::Pkcs7;
use http::HeaderMap;
use http::header::{CONTENT_TYPE, ACCEPT};
use libc::c_char;
use reqwest::blocking::{Client};
use sha2::{Sha512, Digest};
use sha3::{Sha3_512};
use std::ffi::CString;
use std::ffi::CStr;

// create an alias for convinience
type Aes128Ebc = Ecb<Aes128, Pkcs7>;

fn c_str_ptr_to_rust(s: *const c_char) -> &'static str {
    let c_str = unsafe {
        assert!(!s.is_null());

        CStr::from_ptr(s)
    };

    return c_str.to_str().unwrap();
}

fn rust_to_c_str_ptr(s: String) ->  *mut c_char {
    let c_str = CString::new(s).unwrap();
    
    return c_str.into_raw()
}

#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    unsafe {
        if s.is_null() {
            return;
        }
        CString::from_raw(s)
    };
}

#[no_mangle]
pub extern "C" fn base64_encode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let s = base64::encode_config(r_str, base64::STANDARD);

    return rust_to_c_str_ptr(s);
}


#[no_mangle]
pub extern "C" fn base64_decode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let buf = base64::decode_config(r_str, base64::STANDARD).unwrap();

    let s_str = std::str::from_utf8(&buf).unwrap();
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn sha512_encode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let mut hasher = Sha512::new();
    hasher.input(r_str);
    let hash = hasher.result();

    let s_str = format!("{:x}", hash);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn sha3_512_encode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let mut hasher = Sha3_512::new();
    hasher.input(r_str);
    let hash = hasher.result();

    let s_str = format!("{:x}", hash);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn aes_encode() -> *mut c_char {
    let key = hex!("000102030405060708090a0b0c0d0e0f");
    let iv = hex!("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff");
    let plaintext = b"Hello world!";
    let cipher = Aes128Ebc::new_var(&key, &iv).unwrap();
    let ciphertext = cipher.encrypt_vec(plaintext);

    let s_str = format!("{:x}", ciphertext);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn aes_decode() -> *mut c_char {
    let ciphertext = hex!("1b7a4c403124ae2fb52bedc534d82fa8");

    let key = hex!("000102030405060708090a0b0c0d0e0f");
    let iv = hex!("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff");
    let plaintext = b"Hello world!";
    let cipher = Aes128Ebc::new_var(&key, &iv).unwrap();
    let decrypted_ciphertext = cipher.decrypt_vec(&ciphertext).unwrap();

    let s_str = format!("{:x}", decrypted_ciphertext);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn get(c_url: *const c_char) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);

    let resp = reqwest::blocking::get(url);

    let body = match resp {
        Ok(r) =>  r.text(),
        Err(error) => Ok(error.to_string()),
    };

    
    let body = match body {
        Ok(content) => content,
        Err(error) => error.to_string(),
    };

    return rust_to_c_str_ptr(body);
}

#[no_mangle]
pub extern "C" fn post_xml(c_url: *const c_char, c_body: *const c_char) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);
    let body = c_str_ptr_to_rust(c_body);

    let mut headers = HeaderMap::new();

    headers.insert(CONTENT_TYPE, "application/xml".parse().unwrap());
    headers.insert(ACCEPT, "application/xml".parse().unwrap());

    let client = Client::new();

    let resp = client.post(url)
        .headers(headers)
        .body(body)
        .send();

    let body = match resp {
        Ok(r) =>  r.text(),
        Err(error) => Ok(error.to_string()),
    };

    let body = match body {
        Ok(content) => content,
        Err(error) => error.to_string(),
    };

    return rust_to_c_str_ptr(body);
}
