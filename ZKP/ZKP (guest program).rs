#![no_main]

//Write an executable guest program that defines 
//what you want to prove in zero-knowledge.

use risc0_zkvm::{
    guest::env,
    sha::{Impl, Sha256},

};

risc0_zkvm::guest::entry!(main);
//using risc0_zkvm::sha module to hash data
pub fn main(){
    let data: String = env::read();
    let digest =Impl::hash_bytes(&data.as_bytes());
    env::commit(&digest);
}