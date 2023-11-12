use tfhe::boolean::prelude::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
  // We generate the client key and the server key,
  let (client_key, server_key):(ClientKey, ServerKey)  = gen_keys();
  // using the default parameters:
  // let (client_key, server_key): (ClientKey, ServerKey) =
  println!("Generated Keys!");
  // We use the client key to encrypt the messages:
  let ct_1 =  client_key.encrypt(true);
  let ct_2 =  client_key.encrypt(false); 
  //server_key.not(&ct_1);
  println!("Encrypted ciphertexts!");
  // We use the server key to execute the boolean circuit:
  // if ((NOT ct_2) NAND (ct_1 AND ct_2)) then (NOT ct_2) else (ct_1 AND ct_2)
  let ct_3 = server_key.not(&ct_2);
  println!("Evaluated NOT!");
  let ct_4 = server_key.and(&ct_1 , &ct_2);
  println!("Evaluated AND!");
  let ct_5 = server_key.nand(&ct_3, &ct_4);
  println!("Evaluated NAND!");
  // if ((NOT ct_2) NAND (ct_1 AND ct_2)) then (NOT ct_2) else (ct_1 AND ct_2)
  let ct_6 = server_key.mux(&ct_5, &ct_3, &ct_4);
  println!("Evaluated MUX!");
  // Finally, we decrypt the output:
  let output = client_key.decrypt(&ct_6);
  println!("Decrypted result!");
   // And check that the result is the expected one:
   // assert_eq!(output, true);
  assert_eq!(output, true);
  println!("Completed!");
  Ok(())
}
s