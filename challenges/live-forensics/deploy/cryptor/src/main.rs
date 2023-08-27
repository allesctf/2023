use aes::Aes128;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use std::fs::File;
use std::io::Write;
use std::env;
use rand::prelude::*;
use hex;
use md5::{Md5, Digest};

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut hasher = Md5::new();
    hasher.update(&args[1]);

    let key = hasher.finalize();
    let iv = rand::thread_rng().gen::<[u8; 16]>();

    let mut file = File::create("payload_enc.bin").unwrap();
    type Aes128Cbc = Cbc<Aes128, Pkcs7>;

    println!("Key: {}", hex::encode(&key));
    println!("IV: {}", hex::encode(&iv));
    let plaintext = include_bytes!("payload.bin");
    let cipher = Aes128Cbc::new_from_slices(&key, &iv).unwrap();

    // buffer must have enough space for message+padding
    let mut buffer = vec![0u8; 13176696];
    let pos = plaintext.len();
    buffer[..pos].copy_from_slice(plaintext);
    let ciphertext = cipher.encrypt(&mut buffer, pos).unwrap();
    file.write_all(&iv).unwrap();
    file.write_all(&ciphertext).unwrap();
}
