def row_transposition_encrypt(plain_text, key):
    key_order = sorted(range(1, len(key) + 1), key=lambda x: key[x - 1])

    num_columns = len(key)
    num_rows = -(-len(plain_text) // num_columns)  # Ceiling division

    # Create an empty matrix for encryption
    matrix = [[' ' for _ in range(num_columns)] for _ in range(num_rows)]

    # Fill the matrix with the plaintext
    index = 0
    for row in range(num_rows):
        for col in range(num_columns):
            if index < len(plain_text):
                matrix[row][col] = plain_text[index]
                index += 1

    # Read out the matrix column by column to get the ciphertext
    cipher_text = []
    for col in key_order:
        for row in range(num_rows):
            cipher_text.append(matrix[row][col - 1])

    return ''.join(cipher_text)

def row_transposition_decrypt(cipher_text, key):
    key_order = sorted(range(1, len(key) + 1), key=lambda x: key[x - 1])

    num_columns = len(key)
    num_rows = -(-len(cipher_text) // num_columns)  # Ceiling division

    # Calculate the number of characters in the last column
    last_col_chars = len(cipher_text) % num_columns

    # Calculate the number of rows that have the extra character
    rows_with_extra = num_rows - last_col_chars if last_col_chars > 0 else 0

    # Calculate the number of full rows and incomplete rows
    full_rows = num_rows - rows_with_extra
    incomplete_rows = rows_with_extra

    # Calculate the number of characters in the first 'incomplete_rows' columns
    first_incomplete_col_chars = last_col_chars

    # Calculate the number of characters in the remaining 'full_rows' columns
    full_col_chars = num_columns - last_col_chars

    # Create an empty matrix for decryption
    matrix = [[' ' for _ in range(num_columns)] for _ in range(num_rows)]

    index = 0
    for col in key_order:
        if col <= first_incomplete_col_chars:
            for row in range(incomplete_rows):
                matrix[row][col - 1] = cipher_text[index]
                index += 1
        else:
            for row in range(full_rows):
                matrix[row + incomplete_rows][col - 1] = cipher_text[index]
                index += 1

    # Read out the matrix row by row to get the plaintext
    plain_text = []
    for row in range(num_rows):
        for col in range(num_columns):
            plain_text.append(matrix[row][col])

    return ''.join(plain_text)

# Example usage
plaintext = "HELLOWORLD"
key = "3421"
cipher_text = row_transposition_encrypt(plaintext, key)
print("Row Transposition Cipher (Encryption):", cipher_text)

decrypted_text = row_transposition_decrypt(cipher_text, key)
print("Row Transposition Cipher (Decryption):", decrypted_text)
