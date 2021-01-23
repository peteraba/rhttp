extern crate aes_soft as aes;
extern crate base64;
extern crate block_modes;
extern crate hex;
extern crate libc;
extern crate libflate;
extern crate reqwest;
extern crate sha2;
extern crate sha3;

//external crates
use aes::Aes128;
use block_modes::{BlockMode, Ecb};
use block_modes::block_padding::Pkcs7;
use http::HeaderMap;
use http::header::{CONTENT_TYPE, ACCEPT, HeaderValue};
use libc::c_char;
use libflate::gzip::{Encoder, Decoder};
use reqwest::blocking::{Client};
use sha2::{Sha512, Digest};
use sha3::{Sha3_512};
use std::ffi::CString;
use std::ffi::CStr;
use std::io::{self, Read};
use std::str;

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
pub extern "C" fn zip_base64_encode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);
    let r_bytes = r_str.as_bytes();

    let mut encoder = Encoder::new(Vec::new()).unwrap();
    io::copy(&mut &r_bytes[..], &mut encoder).unwrap();
    let encoded_data = encoder.finish().into_result().unwrap();

    let s = base64::encode(encoded_data);

    return rust_to_c_str_ptr(s);
}


#[no_mangle]
pub extern "C" fn zip_base64_decode(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let buf = base64::decode_config(r_str, base64::STANDARD).unwrap();

    let mut decoder = Decoder::new(&buf[..]).unwrap();
    let mut decoded_data = Vec::new();
    decoder.read_to_end(&mut decoded_data).unwrap();

    let s_str = std::str::from_utf8(&decoded_data).unwrap();
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn sha512_hash(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let mut hasher = Sha512::new();
    hasher.update(r_str);
    let hash = hasher.finalize();

    let s_str = format!("{:x}", hash);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn sha3_512_hash(s: *const c_char) -> *mut c_char {
    let r_str = c_str_ptr_to_rust(s);

    let mut hasher = Sha3_512::new();
    hasher.update(r_str);
    let hash = hasher.finalize();

    let s_str = format!("{:x}", hash);
    
    return rust_to_c_str_ptr(s_str.to_string());
}

#[no_mangle]
pub extern "C" fn aes_encrypt(c_plaintext: *const c_char, c_key: *const c_char, flags: i32) -> *mut c_char {
    let uflags = flags as u32;
    let input = decode_c(c_plaintext, uflags);
    let key = decode_c(c_key, uflags >> 4);

    let ciphertext = create_cipher(key).encrypt_vec(input.as_slice());
   
    return rust_to_c_str_ptr(encode_c(ciphertext, uflags >> 2));
}

#[no_mangle]
pub extern "C" fn aes_decrypt(c_ciphertext: *const c_char, c_key: *const c_char, flags: i32) -> *mut c_char {
    let uflags = flags as u32;
    let input = decode_c(c_ciphertext, uflags);
    let key = decode_c(c_key, uflags >> 4);

    let plaintext = create_cipher(key).decrypt_vec(input.as_slice()).unwrap();

    return rust_to_c_str_ptr(encode_c(plaintext, uflags >> 2));
}

#[no_mangle]
pub extern "C" fn get_plain(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);

    let resp = reqwest::blocking::get(url);

    let status = match &resp {
        Ok(r) => r.status().as_u16() as i32,
        Err(_) => 0,
    };

    *code_ref = status;

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
pub extern "C" fn get_xml(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);

    let mut headers = HeaderMap::new();

    headers.insert(CONTENT_TYPE, "application/xml".parse().unwrap());
    headers.insert(ACCEPT, "application/xml".parse().unwrap());

    return get_inner(url, headers, code_ref);
}

#[no_mangle]
pub extern "C" fn get_json(c_url: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);

    let mut headers = HeaderMap::new();

    headers.insert(CONTENT_TYPE, "application/json".parse().unwrap());
    headers.insert(ACCEPT, "application/json".parse().unwrap());

    return get_inner(url, headers, code_ref);
}

fn get_inner(url:  &'static str, headers: HeaderMap, code_ref: &mut i32) -> *mut c_char {
    let client = Client::new();

    let resp = client.get(url)
        .headers(headers)
        .send();

    let status = match &resp {
        Ok(r) => r.status().as_u16() as i32,
        Err(_) => 0,
    };

    *code_ref = status;

    let body = match resp {
        Ok(r) =>  r.text(),
        Err(error) => Ok(error.to_string()),
    };

    let content = match body {
        Ok(content) => content,
        Err(error) => error.to_string(),
    };

    return rust_to_c_str_ptr(content);
}

#[no_mangle]
pub extern "C" fn post_plain(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);
    let body = c_str_ptr_to_rust(c_body);

    let headers = HeaderMap::new();

    return post_inner(url, body, headers, code_ref);
}

#[no_mangle]
pub extern "C" fn post_xml(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);
    let body = c_str_ptr_to_rust(c_body);

    let mut headers = HeaderMap::new();

    headers.insert(CONTENT_TYPE, "application/xml".parse().unwrap());
    headers.insert(ACCEPT, "application/xml".parse().unwrap());

    return post_inner(url, body, headers, code_ref);
}

#[no_mangle]
pub extern "C" fn post_json(c_url: *const c_char, c_body: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);
    let body = c_str_ptr_to_rust(c_body);

    let mut headers = HeaderMap::new();

    headers.insert(CONTENT_TYPE, "application/json".parse().unwrap());
    headers.insert(ACCEPT, "application/json".parse().unwrap());


    return post_inner(url, body, headers, code_ref);
}

#[no_mangle]
pub extern "C" fn post_custom(c_url: *const c_char, c_body: *const c_char, c_headers_joined: *const c_char, code_ref: &mut i32) -> *mut c_char {
    let url = c_str_ptr_to_rust(c_url);
    let body = c_str_ptr_to_rust(c_body);
    let headers_joined = c_str_ptr_to_rust(c_headers_joined);

    let headers = get_headers(headers_joined);

    return post_inner(url, body, headers, code_ref)
}

fn post_inner(url:  &'static str, body:  &'static str, headers: HeaderMap, code_ref: &mut i32) -> *mut c_char {
    let client = Client::new();

    let resp = client.post(url)
        .headers(headers)
        .body(body)
        .send();

    let status = match &resp {
        Ok(r) => r.status().as_u16() as i32,
        Err(_) => 0,
    };

    *code_ref = status;

    let body = match resp {
        Ok(r) =>  r.text(),
        Err(error) => Ok(error.to_string()),
    };

    let content = match body {
        Ok(content) => content,
        Err(error) => error.to_string(),
    };

    return rust_to_c_str_ptr(content);
}

fn get_headers(headers_joined: &'static str) -> HeaderMap {
    let mut headers = HeaderMap::new();

    for header_line in headers_joined.split("\n") {
        let header_parts: Vec<&str> = header_line.split(":").collect();

        if header_parts.len() != 2 {
            continue;
        }

        headers.insert(header_parts[0], HeaderValue::from_str(header_parts[1]).unwrap());
    }

    return headers;
}

fn decode_c(c_input: *const c_char, flags: u32) -> Vec<u8> {
    let input = c_str_ptr_to_rust(c_input);

    if flags % 2 == 1 {
        return hex::decode(input).unwrap();
    }

    if (flags >> 1) % 2 == 1 {
        return base64::decode_config(input, base64::STANDARD).unwrap();
    }

    return String::from(input).into_bytes();
}

fn encode_c(raw: Vec<u8>, flags: u32) -> String {
    if flags % 2 == 1 {
        return hex::encode(raw);
    }
    
    if (flags >> 1) % 2 == 1 {
        return base64::encode_config(raw, base64::STANDARD);
    }

    return String::from_utf8(raw).unwrap();
}

fn create_cipher(key: Vec<u8>) -> Ecb::<Aes128, Pkcs7> {
    let iv = Default::default();

    return Ecb::<Aes128, Pkcs7>::new_var(key.as_slice(), iv).unwrap();
}

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