import string

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def multiplicative_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(plain_text, a, b):
    alphabet = string.ascii_lowercase
    m = len(alphabet)

    cipher_text = ''
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                char = char.lower()
                shift = (a * (alphabet.index(char)) + b) % m
                encrypted_char = alphabet[shift].upper()
            else:
                shift = (a * (alphabet.index(char)) + b) % m
                encrypted_char = alphabet[shift]
            cipher_text += encrypted_char
        else:
            cipher_text += char

    return cipher_text

def affine_decrypt(cipher_text, a, b):
    alphabet = string.ascii_lowercase
    m = len(alphabet)

    # Calculate the multiplicative inverse of 'a' modulo 'm'
    if gcd(a, m) != 1:
        raise ValueError("The 'a' value is not relatively prime to the alphabet size.")

    a_inverse = multiplicative_inverse(a, m)
    if a_inverse is None:
        raise ValueError("The multiplicative inverse of 'a' does not exist.")

    plain_text = ''
    for char in cipher_text:
        if char.isalpha():
            if char.isupper():
                char = char.lower()
                shift = (a_inverse * (alphabet.index(char) - b)) % m
                decrypted_char = alphabet[shift].upper()
            else:
                shift = (a_inverse * (alphabet.index(char) - b)) % m
                decrypted_char = alphabet[shift]
            plain_text += decrypted_char
        else:
            plain_text += char

    return plain_text

# Example usage
plaintext = "HELLO"
a = 5  # Choose an integer a such that gcd(a, 26) = 1
b = 8  # Choose an integer b
cipher_text = affine_encrypt(plaintext, a, b)
print("Affine Cipher (Encryption):", cipher_text)

decrypted_text = affine_decrypt(cipher_text, a, b)
print("Affine Cipher (Decryption):", decrypted_text)
