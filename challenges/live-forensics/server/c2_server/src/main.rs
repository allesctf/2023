#[macro_use] extern crate rocket;
use std::fs::File;
use std::env;
use std::fs::OpenOptions;
use std::io::Write;
use std::io::{self, BufRead};
use std::path::Path;
use hex_literal::hex;
use rc4::{consts::*, KeyInit, StreamCipher};
use rc4::{Key, Rc4, Rc4Core};


#[derive(Debug)]
struct Agent {
    id: String,
    key: String
}

impl Agent {
    fn from_string(line: String) -> Option<Agent> {
	let v: Vec<&str> = line.split(":").collect();
	match v.len() {
	    2 => Some(
		Agent{
		    id: v[0].to_string(),
		    key: v[1].to_string()
		}),
	    _ => None
	}
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn get_all_agents() -> Option<Vec<Agent>> {
    let mut agents: Vec<Agent> = Vec::new();
    if let Ok(lines) = read_lines("./agents.txt") {
        for line in lines {
            if let Ok(s) = line {
                match Agent::from_string(s) {
		    Some(agent) => agents.push(agent),
		    _ => {}	
		}
            }
        }
	return Some(agents);
    }
    None
}

#[get("/register_agent/<agent_id>")]
fn register_agent(agent_id: &str) -> String {
    match env::var("MODE") {
	Ok(val) => {
	    if val == "SETUP" {
		let mut fileRef = OpenOptions::new().append(true).open("agents.txt").expect("Unable to open file");
		fileRef.write_all(format!("{}:whats_the_pw?\n", agent_id).as_bytes()).expect("write failed");
	    }
	},
	_ => ()
    }

    
    format!("Welcome {}! This server uses payload keying to prevent connections from sandboxes or analysts! 
For security all communication will be encrypted after key exchange. Call /get_flag to test the encrypted communication.", agent_id)
}

#[get("/get_enc_key/<agent_id>")]
fn get_key(agent_id: &str) -> String {
    if let Some(agents) = get_all_agents() {
	for agent in agents {
	    if agent.id.eq(agent_id){
		return format!("RC4_ENC_KEY:{}", &agent.key);
	    }
	}
    }
    "Unknwon agent... SHUTDOWN!".to_string()
}

#[get("/get_commands/<agent_id>")]
fn get_commands(agent_id: &str) -> String {
   if let Some(agents) = get_all_agents() {
	for agent in agents {
	    if agent.id.eq(agent_id){
		let mut key= [0u8; 13];
		if agent.key.len() != key.len() {
		    return "Key error...".to_string()
		}
		agent.key.bytes()
		    .zip(key.iter_mut())
		    .for_each(|(b, ptr)| *ptr = b);
		let mut rc4 = Rc4::new(&key.into());
		let mut data = b"No now commands yet...".to_vec();
		rc4.apply_keystream(&mut data);
		return base64::encode(data);
	    }
	}
   }
    "Agent not known. Go away!".to_string()
}

#[get("/get_flag/<agent_id>")]
fn get_flag(agent_id: &str) -> String {
    if let Some(agents) = get_all_agents() {
	for agent in agents {
	    if agent.id.eq(agent_id){
		let mut key= [0u8; 13];
		if agent.key.len() != key.len() {
		    return "Key error...".to_string()
		}
		agent.key.bytes()
		    .zip(key.iter_mut())
		    .for_each(|(b, ptr)| *ptr = b);
		let mut rc4 = Rc4::new(&key.into());
		let mut data = b"ALLES!{Th3_p4s5w0rd_i5_'infected'!}".to_vec();
		rc4.apply_keystream(&mut data);
		return format!("ENC_FLAG:{}", base64::encode(data));
	    }
	}
    }
    "Agent not known. Go away!".to_string()
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![register_agent, get_key, get_flag, get_commands])
}
