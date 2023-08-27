use std::io::{Read, Write};
use std::{fs, io};

fn encrypt_block(block: &mut [u8]) {
    let mut key = 0usize;
    let b: *const _ = &key;

    key = b as usize;

    if block.len() > 8 {
        encrypt_block(&mut block[8..])
    }

    for i in 0..block.len() {
        let seed = key + 28411;
        for _ in 0..8121 {
            key = (seed + key) % 134456
        }

        block[i] ^= key as u8
    }
}

fn encrypt_file(entry: fs::DirEntry) -> io::Result<()> {
    let mut data = vec![];
    {
        let mut fin = fs::File::open(entry.path())?;
        fin.read_to_end(&mut data)?;
    }

    encrypt_block(&mut data);

    let mut fout = fs::File::create(entry.path())?;
    fout.write_all(&data)?;

    Ok(())
}

fn main() -> io::Result<()> {
    for entry in fs::read_dir(".")? {
        let entry = entry?;
        if !entry.path().is_dir()
            && entry
                .file_name()
                .to_str()
                .map_or(false, |name| name == "flag.txt")
        {
            encrypt_file(entry)?;
        }
    }

    unsafe {
        let x: *mut usize = 0x1337 as *mut usize;
        *x = 0;
    }

    Ok(())
}
