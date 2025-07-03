from flask import Flask, render_template, request, send_file
from cipher.encrypt import encrypt_message
from cipher.decrypt import decrypt_message
from cipher.utils import save_key_as_pdf, get_max_key_size
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    decrypted = None
    error = None
    max_key = 1

    if request.method == 'POST':
        raw_text = request.form['text']
        processed_text = raw_text.replace(' ', '_').upper()
        key_size = int(request.form['key_size'])
        key_mode = request.form['key_mode']
        key_input = request.form.get('key_input')
        action = request.form['action']
        max_key = get_max_key_size(processed_text)

        if action == 'Encrypt':
            try:
                result, key_matrix, max_key = encrypt_message(processed_text, key_size, key_mode, key_input)
                save_key_as_pdf(key_matrix)
                original_length = len(processed_text)
                with open("original_length.txt", "w") as f:
                    f.write(str(original_length))
            except ValueError as ve:
                error = f"Error: {ve}"
        elif action == 'Decrypt':
            try:
                encrypted_text = request.form['text']
                key_matrix = eval(request.form['key_input'])
                with open("original_length.txt", "r") as f:
                    original_length = int(f.read().strip())
                decrypted = decrypt_message(encrypted_text, key_matrix, original_length)
            except Exception as e:
                error = f"Decryption Error: {e}"

    return render_template('index.html', result=result, decrypted=decrypted, error=error, max_key=max_key)

@app.route('/download-key')
def download_key():
    return send_file('key.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
