def rail_fence_encrypt(plain_text, num_rails):
    # Create an empty rail fence matrix
    fence = [[' ' for _ in range(len(plain_text))] for _ in range(num_rails)]

    # Fill in the matrix with the plaintext characters
    row, col, direction = 0, 0, 1
    for char in plain_text:
        fence[row][col] = char
        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1
        row += direction
        col += 1

    # Read the matrix column by column to get the ciphertext
    cipher_text = []
    for i in range(num_rails):
        cipher_text.extend(fence[i])

    return ''.join(cipher_text)

def rail_fence_decrypt(cipher_text, num_rails):
    # Create an empty rail fence matrix
    fence = [[' ' for _ in range(len(cipher_text))] for _ in range(num_rails)]

    # Calculate the number of characters in each rail
    rail_lengths = [0] * num_rails
    row, col, direction = 0, 0, 1
    for _ in cipher_text:
        rail_lengths[row] += 1
        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1
        row += direction

    # Fill in the matrix with 'x' to mark the rail positions
    index = 0
    for i in range(num_rails):
        for j in range(rail_lengths[i]):
            fence[i][j] = 'x'

    # Populate the 'x' positions with characters from the ciphertext
    for i in range(num_rails):
        for j in range(rail_lengths[i]):
            fence[i][j] = cipher_text[index]
            index += 1

    # Read the matrix in zigzag order to get the plaintext
    row, col, direction = 0, 0, 1
    plain_text = []
    for _ in range(len(cipher_text)):
        plain_text.append(fence[row][col])
        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1
        row += direction
        col += 1

    return ''.join(plain_text)

# Example usage
plaintext = "HELLOWORLD"
num_rails = 3
cipher_text = rail_fence_encrypt(plaintext, num_rails)
print("Rail Fence Cipher (Encryption, {} rails): {}".format(num_rails, cipher_text))

decrypted_text = rail_fence_decrypt(cipher_text, num_rails)
print("Rail Fence Cipher (Decryption, {} rails): {}".format(num_rails, decrypted_text))
