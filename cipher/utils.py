# cipher/utils.py
import numpy as np
import random
from fpdf import FPDF
import math

def text_to_numbers(text):
    return [26 if char == ' ' else ord(char.upper()) - 65 for char in text]

def numbers_to_text(numbers):
    return ''.join(' ' if num == 26 else chr(num + 65) for num in numbers)

def generate_random_matrix(n):
    while True:
        matrix = np.random.randint(0, 27, size=(n, n))  # Updated to handle mod 27
        det = int(round(np.linalg.det(matrix))) % 27
        if np.gcd(det, 27) == 1:
            return matrix.tolist()

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def save_key_as_pdf(matrix):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hill Cipher Key Matrix", ln=1, align='C')
    pdf.ln(10)
    matrix_string = ',\n'.join([str(row) for row in matrix])
    pdf.multi_cell(0, 10, txt=f"Key Matrix (copy-paste ready):\n[{matrix_string}]")
    pdf.output("key.pdf")

def get_max_key_size(text):
    cleaned = text.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    return int(math.floor(len(cleaned) ** 0.5))