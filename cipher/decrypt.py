# cipher/decrypt.py
import numpy as np
from .utils import mod_inverse, text_to_numbers, numbers_to_text

def decrypt_message(encrypted_text, key_matrix, original_length=None):
    key_size = len(key_matrix)
    encrypted_text = encrypted_text.strip().replace('\n', '').replace('\r', '')
    numbers = text_to_numbers(encrypted_text)

    if len(numbers) % key_size != 0:
        raise ValueError("Encrypted message length must be divisible by the key size.")

    chunks = [numbers[i:i+key_size] for i in range(0, len(numbers), key_size)]

    matrix = np.array(key_matrix)
    det = int(round(np.linalg.det(matrix)))
    det_mod_27 = det % 27
    if np.gcd(det_mod_27, 27) != 1:
        raise ValueError("Key matrix is not invertible modulo 27. Please use an auto-generated key.")

    det_inv = mod_inverse(det_mod_27, 27)
    if det_inv is None:
        raise ValueError("Key matrix is not invertible")

    adj = np.round(det * np.linalg.inv(matrix)).astype(int) % 27
    inv_matrix = (det_inv * adj) % 27

    decrypted_chunks = [np.dot(inv_matrix, np.array(chunk)) % 27 for chunk in chunks]
    decrypted_numbers = [int(item) for chunk in decrypted_chunks for item in chunk]

    plain_text = numbers_to_text(decrypted_numbers)
    return plain_text[:original_length] if original_length else plain_text