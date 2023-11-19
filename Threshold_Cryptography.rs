use threshold_crypto::{PublicKeyShare, SecretKeySet, SecretKeyShare, Signature, SignatureShare};
//good refrence: https://docs.rs/threshold_crypto/0.4.0/threshold_crypto/struct.PublicKeySet.html

fn main() {
  // Instantiate a random number generator
  let mut rng = rand::thread_rng();

  // Generate key sets
  let sk_set =  SecretKeySet::random(3, &mut rng);
  
  // Generate a public key from the secret key set
  let pk_set = sk_set.public_keys();
  
  // Generate key shares
   let sk_shares: Vec<SecretKeyShare> = (0..5).map(|i| sk_set.secret_key_share(i)).collect();
  
   let pk_shares: Vec<PublicKeyShare> =(0..5).map(|i| pk_set.public_key_share(i)).collect();
  
  // Instantiate the message
  let message = b"Welcome to crypto!";
  
  // Create three signature shares on the message
   let sig_shares: Vec<(usize, SignatureShare)> =(0..3).map(|i| (i, sk_shares[i].sign(message))).collect();
  
  assert_eq!(sig_shares.len(), 3);
  
  // Validate the signature shares.
  for (i, sig_share) in &sig_shares {
    assert!(pk_shares[*i].verify(sig_share, message));
  }
  
  // Combine the signature shares
   let signature: Result<Signature, _> = pk_set.combine_signatures(sig_shares.iter().map(|(i,s)|(*i,s)));
  
  // Validate the signature.
  let valid_signature = signature
    .expect("Failed to combine signature shares.");
  assert!(pk_set.public_key().verify(&valid_signature, message));
  
  println!("Complete!")
}
