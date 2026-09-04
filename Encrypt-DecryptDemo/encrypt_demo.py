# Victor Delgado
# SDEV 200 - Module 2 Assignment
# Encrypt/Decrypt Demo
# ---------------------------------------------------------
# This version lets the user type a message and shows how long
# encryption takes for both symmetric and asymmetric methods.
# ---------------------------------------------------------

import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

OUTPUT_FILE = "demo_output.txt"


def symmetric_demo(message):
    # Generate a random key for Fernet (AES under the hood)
    symmetric_key = Fernet.generate_key()
    cipher = Fernet(symmetric_key)

    # Time the encryption
    start = time.time()
    encrypted = cipher.encrypt(message.encode())
    end = time.time()
    enc_time = end - start

    # Decrypt the message
    decrypted = cipher.decrypt(encrypted)

    return {
        "key": symmetric_key.decode(),
        "input": message,
        "ciphertext": encrypted.decode(),
        "output": decrypted.decode(),
        "time": enc_time,
    }


def asymmetric_demo(message):
    # Generate RSA private/public key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Time the encryption
    start = time.time()
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    end = time.time()
    enc_time = end - start

    # Decrypt with private key
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Export keys in PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()

    return {
        "private_key": private_pem,
        "public_key": public_pem,
        "input": message,
        "ciphertext": encrypted.hex(),
        "output": decrypted.decode(),
        "time": enc_time,
    }


def write_report(sym, asym):
    report = f"""
============================
SYMMETRIC ENCRYPTION (Fernet)
============================
Key: {sym['key']}
Input: {sym['input']}
Ciphertext: {sym['ciphertext']}
Output: {sym['output']}
Encryption Time: {sym['time']:.6f} seconds

===========================
ASYMMETRIC ENCRYPTION (RSA)
===========================
Private Key:
{asym['private_key']}

Public Key:
{asym['public_key']}

Input: {asym['input']}
Ciphertext: {asym['ciphertext']}
Output: {asym['output']}
Encryption Time: {asym['time']:.6f} seconds
""".strip()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as report_file:
        report_file.write(report)

    return report


if __name__ == "__main__":
    # Let the user type a message
    user_message = input("Enter a message to encrypt: ")

    # Run both demos
    symmetric_result = symmetric_demo(user_message)
    asymmetric_result = asymmetric_demo(user_message)

    # Write everything to a text file
    report_text = write_report(symmetric_result, asymmetric_result)

    # Print to console
    print("\n" + report_text)
    print(f"\nReport saved to {OUTPUT_FILE}")
