fn main(){

    //Write an executable host program that creates 
    //zero-knowledge proofs of your guest’s executions


    //take the command
    let matches=Command::new("hash")
    .arg(Arg::new("message").default_value(""))
    .get_matches();

    let message=matches.get_one::<String>("message").unwrap();

    //prove hash message
    let (digest ,receipt)=provably_hash(message , false);

    //verify receipt, ensuring prover knows valid SHA-256 preimage

    receipt.verify(HASH_ID);.expect("receipt verification failed");

    println!("I provably know data whose SHA-256 hash is {}", digest);






}