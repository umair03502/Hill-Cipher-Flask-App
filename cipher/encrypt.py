# cipher/encrypt.py
import numpy as np
import random
from .utils import mod_inverse, generate_random_matrix, text_to_numbers, numbers_to_text, get_max_key_size

def encrypt_message(text, key_size, key_mode, key_input=None):
    # Convert to uppercase but keep spaces (spaces will be handled as 26)
    text = text.upper()

    max_key_size = get_max_key_size(text)
    if key_size > max_key_size:
        raise ValueError(f"Key size too large for message length. Max allowed: {max_key_size}")

    text_numbers = text_to_numbers(text)
    while len(text_numbers) % key_size != 0:
        text_numbers.append(23)  # Padding with 'X'

    if key_mode == 'auto':
        key_matrix = generate_random_matrix(key_size)
    else:
        key_matrix = eval(key_input)
        matrix = np.array(key_matrix)
        det = int(round(np.linalg.det(matrix))) % 26
        if np.gcd(det, 26) != 1:
            raise ValueError("Manually entered key matrix is not invertible modulo 26. Please use auto-generated key.")

    matrix = np.array(key_matrix)
    chunks = [text_numbers[i:i+key_size] for i in range(0, len(text_numbers), key_size)]
    encrypted_chunks = [np.dot(matrix, np.array(chunk)) % 27 for chunk in chunks]  # Use mod 27 to support space
    encrypted_numbers = [item for sublist in encrypted_chunks for item in sublist]
    encrypted_text = numbers_to_text(encrypted_numbers)
    return encrypted_text, matrix.tolist(), max_key_size