use sha2::{Digest , Sha256};
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////traits
pub trait SumCommitmentTrait {
fn amount(&self) -> u64;
fn digest(&self) -> [u8; 32];
}

pub trait ExclusiveAllotmentProofTrait <C: SumCommitmentTrait > {
fn position(&self) -> usize;
fn sibling(&self , height: u8) -> Option <C>;
fn verify(&self , root_commitment: &C) -> bool;
}

pub trait MerkleTreeTrait <C: SumCommitmentTrait , P: ExclusiveAllotmentProofTrait <C>> {
fn new(values: Vec<u64 >) -> Self;
fn commit(&self) -> C;
fn prove(&self , position: usize) -> P;
}

fn hash_bytes(slice: &[u8]) -> [u8; 32] {
let mut hasher = Sha256::new();
hasher.update(slice);
hasher.finalize().into()
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////struct
pub struct SumCommitment {
    amount: u64,
    digest: [u8; 32],
}

pub struct ExclusiveAllotmentProof {
    position: usize,
    sibling: Option<SumCommitment>,
}

pub struct MerkleTree {
    values: Vec<u64>,
    root_commitment: SumCommitment,
}





///////////////////////////////////////////////////////////////////////////////////////////////////////// SumCommitment
impl SumCommitment{//SumCommitment
    fn new(amount: u64, digest: [u8; 32]) -> Self {
        SumCommitment { amount, digest }
    }
}
impl SumCommitmentTrait for SumCommitment {
    fn amount(&self) -> u64 {
        self.amount
    }
    fn digest(&self) -> [u8; 32] {
        self.digest
    }
}
///////////////////////////////////////////////////////////////////////////////////////////////////////// ExclusiveAllotmentProof
impl ExclusiveAllotmentProof{
    fn new(position: usize, sibling: Option<SumCommitment>) -> Self {
    ExclusiveAllotmentProof { position, sibling }
    }
}
impl ExclusiveAllotmentProofTrait<SumCommitment > for ExclusiveAllotmentProof {

    fn position(&self) -> usize {
        self.position
    }

    fn sibling(&self) -> Option<SumCommitment> {
        self.sibling.clone()
    }

    fn verify<C: SumCommitmentTrait>( proof: &ExclusiveAllotmentProof,root_commitment: &C,leaf_commitment: &C,height: u8,) -> bool {
        if height == 0 {
            // If we're at the leaf, the sibling should be the leaf commitment
            return match &proof.sibling {Some(sibling) => sibling.digest() == leaf_commitment.digest(),None => false};
        } else {
            // If not at the leaf, verify the sibling commitment
            let sibling_commitment = match &proof.sibling {Some(sibling) => sibling,None => return false};
            // Calculate the hash of the combined commitments
            let combined_digest = hash_bytes(&[&root_commitment.digest(),&sibling_commitment.digest()].concat());
            // Recursively verify the proof with updated commitments
            return Self::verify(proof,&SumCommitment::new(leaf_commitment.amount() + sibling_commitment.amount(), combined_digest),leaf_commitment,height - 1);
        }
    }
}


///////////////////////////////////////////////////////////////////////////////////////////////////////// MerkleTree
impl MerkleTree {
        // Recursive function to build the Merkle tree
        fn build_merkle_tree<C: SumCommitmentTrait>(&self,values: &Vec<u64>,height: u8,) -> SumCommitment {
            if height == 0 {
                // Reached the leaf level, use the leaf value
                let leaf_value = values[0];
                let leaf_digest = hash_bytes(&(leaf_value.to_be_bytes().to_vec()));
                return SumCommitment::new(leaf_value, leaf_digest);
            } 
            else {
                // Divide the values into left and right halves
                let mid = values.len() / 2;
                let left_values = values[..mid].to_vec();
                let right_values = values[mid..].to_vec();
                // Recursively build the left and right subtrees
                let left_commitment = self.build_merkle_tree(&left_values, height - 1);
                let right_commitment = self.build_merkle_tree(&right_values, height - 1);
                // Calculate the combined commitment
                let combined_digest = hash_bytes(&[&left_commitment.digest(), &right_commitment.digest(),].concat());
                // Return the commitment for this level
                SumCommitment::new(left_commitment.amount() + right_commitment.amount(),combined_digest)
            }
        }

}

impl MerkleTreeTrait< SumCommitment, ExclusiveAllotmentProof<SumCommitment>> for MerkleTree {
    fn new(values: Vec<u64>) -> Self {
        let root_commitment = Self::build_tree(&values);
        MerkleTree {values,root_commitment}
    }
    fn commit(&self) -> SumCommitment {
        // Return the precomputed root commitment
        self.root_commitment.clone()
    }
    
    fn prove(&self, position: usize) -> ExclusiveAllotmentProof {

        // Converting the position to a binary representation
        let position_binary = format!("{:b}", position);

        // Create a mutable copy of the values vector for building the proof
        let mut values = self.values.clone();

        // Initialize the proof and height
        let mut proof = ExclusiveAllotmentProof::new(position, None);
        let mut height = 0;

        // Start constructing the proof
        while !position_binary.is_empty() {
            // Check the last bit of the position
            if position_binary.ends_with("0") {
                // If the last bit is 0, the sibling is to the right
                let sibling_position = position + 1;
                if sibling_position < values.len() {
                    // Calculate the combined digest for this level
                    let sibling_value = values[sibling_position];
                    let sibling_digest = hash_bytes(&(sibling_value.to_be_bytes().to_vec()));
                    let combined_digest = hash_bytes(&[&values[position].to_be_bytes().to_vec(),&sibling_digest].concat());
                    // Create a SumCommitment for the sibling
                    let sibling_commitment = SumCommitment::new(sibling_value, sibling_digest);
                    // Update the proof and values
                    proof.sibling = Some(sibling_commitment);
                    values[position] = combined_digest;
                }
            } else {
                // If the last bit is 1, the sibling is to the left
                let sibling_position = position - 1;
                if sibling_position >= 0 && sibling_position < values.len() {
                    // Calculate the combined digest for this level
                    let sibling_value = values[sibling_position];
                    let sibling_digest = hash_bytes(&(sibling_value.to_be_bytes().to_vec()));
                    let combined_digest = hash_bytes(&[&sibling_digest,&values[position].to_be_bytes().to_vec()].concat());

                    // Create a SumCommitment for the sibling
                    let sibling_commitment = SumCommitment::new(sibling_value, sibling_digest);

                    // Update the proof and values
                    proof.sibling = Some(sibling_commitment);
                    values[position] = combined_digest;
                }
            }
            // Remove the last bit from the position and increment the height
            position_binary.pop();
            height += 1;
        }
        proof
    }

}


/////////////////////////////////////////////////////////////////////////////////////////////////////////



fn main() {
    // Example usage of the Merkle tree commitment scheme
    let values = vec![10, 20, 30, 40, 50];
    let merkle_tree = MerkleTree::new(values.clone());
    let root_commitment = merkle_tree.commit();
    // Generate a proof for a specific position in the tree
    let position_to_prove = 2;
    let proof = merkle_tree.prove(position_to_prove);
    // Verify the proof against the root commitment
    let is_proof_valid = proof.verify(&root_commitment);
        println!("Proof is valid: {}",is_proof_valid);
}