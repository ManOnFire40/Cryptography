import string

def monoalphabetic_encrypt(plain_text, key):
    # Create a mapping from the alphabet to the key
    alphabet = string.ascii_lowercase
    key = key.lower()
    mapping = {}
    for i in range(len(alphabet)):
        mapping[alphabet[i]] = key[i]

    # Encrypt the plaintext
    cipher_text = ''
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                cipher_text += mapping[char.lower()].upper()
            else:
                cipher_text += mapping[char]
        else:
            cipher_text += char

    return cipher_text

def monoalphabetic_decrypt(cipher_text, key):
    # Create a mapping from the key to the alphabet
    alphabet = string.ascii_lowercase
    key = key.lower()
    mapping = {}
    for i in range(len(key)):
        mapping[key[i]] = alphabet[i]

    # Decrypt the ciphertext
    plain_text = ''
    for char in cipher_text:
        if char.isalpha():
            if char.isupper():
                plain_text += mapping[char.lower()].upper()
            else:
                plain_text += mapping[char]
        else:
            plain_text += char

    return plain_text

# Example usage
plaintext = "HELLO"
key = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
cipher_text = monoalphabetic_encrypt(plaintext, key)
print("Monoalphabetic Cipher (Encryption):", cipher_text)

decrypted_text = monoalphabetic_decrypt(cipher_text, key)
print("Monoalphabetic Cipher (Decryption):", decrypted_text)
