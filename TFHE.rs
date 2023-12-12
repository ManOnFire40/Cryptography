use tfhe::shortint::prelude::*;

fn query(key: ServerKey, mut target: Ciphertext, inventory: &[(u8, u8)]) -> Ciphertext {
    //ServerKey used for homomorphic computation
    //target ciphertext corresponding to the item code
    //inventory  plaintext list of all (item, amount) pairs present in the inventory.

 // let final_amount;
  //for ( id,amount ) in inventory

  //let is_found = EQAUL( id , target ) return 1 or 0 
  //let curr_amount = MULTIPLY (amount , is_found  )
  //ADD(curr_amount , final_amount)


let initial = 0; //cummulative amount since ID iss not unique within inventory
let combined_target_final_amount = key.unchecked_scalar_add(&mut target, initial);
let mut final_amount = key.unchecked_sub(&combined_target_final_amount, &mut target);
  //previous lines is to encrypt zero value

for (id,amount) in inventory{

    let mut curr_condition=key.smart_scalar_equal(&mut target ,*id);
    let mut curr_amount=key.smart_scalar_mul(&mut curr_condition,*amount);
    final_amount=key.smart_add(&mut final_amount,&mut curr_amount);

}
return final_amount;
}

fn main() {
    // nothing to do here
}

#[cfg(test)]
mod tests {
    use tfhe::shortint::parameters::PARAM_MESSAGE_4_CARRY_0_KS_PBS;
    use tfhe::shortint::prelude::*;

    use crate::query;

    #[test]
    fn test_it() {
        let (client_key, server_key) = gen_keys(PARAM_MESSAGE_4_CARRY_0_KS_PBS);

        let item_code = 2u8;

        let item_code_ciphertext = client_key.encrypt(item_code as u64);

        let stock_ciphertext = query(server_key, item_code_ciphertext, &[(1, 2), (2, 1),(1, 2) ]);

        let stock_count = client_key.decrypt(&stock_ciphertext);

        assert_eq!(stock_count, 4);
    }
}