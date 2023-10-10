import string

def vigenere_encrypt(plain_text, key):
    # Create a key that repeats to match the length of the plaintext
    key = key.lower()
    key_repeated = key * (len(plain_text) // len(key)) + key[:len(plain_text) % len(key)]

    # Encrypt the plaintext
    cipher_text = ''
    for i in range(len(plain_text)):
        if plain_text[i].isalpha():
            shift = ord(key_repeated[i]) - ord('a')
            if plain_text[i].isupper():
                encrypted_char = chr(((ord(plain_text[i]) - ord('A') + shift) % 26) + ord('A'))
            else:
                encrypted_char = chr(((ord(plain_text[i]) - ord('a') + shift) % 26) + ord('a'))
            cipher_text += encrypted_char
        else:
            cipher_text += plain_text[i]

    return cipher_text

def vigenere_decrypt(cipher_text, key):
    # Create a key that repeats to match the length of the ciphertext
    key = key.lower()
    key_repeated = key * (len(cipher_text) // len(key)) + key[:len(cipher_text) % len(key)]

    # Decrypt the ciphertext
    plain_text = ''
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift = ord(key_repeated[i]) - ord('a')
            if cipher_text[i].isupper():
                decrypted_char = chr(((ord(cipher_text[i]) - ord('A') - shift + 26) % 26) + ord('A'))
            else:
                decrypted_char = chr(((ord(cipher_text[i]) - ord('a') - shift + 26) % 26) + ord('a'))
            plain_text += decrypted_char
        else:
            plain_text += cipher_text[i]

    return plain_text

# Example usage
plaintext = "HELLO"
key = "KEY"
cipher_text = vigenere_encrypt(plaintext, key)
print("Vigenère Cipher (Encryption):", cipher_text)

decrypted_text = vigenere_decrypt(cipher_text, key)
print("Vigenère Cipher (Decryption):", decrypted_text)
