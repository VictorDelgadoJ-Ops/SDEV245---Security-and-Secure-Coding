"""A02: Cryptographic Failures.

Original problem: SHA-1 is a fast password hash that is easier to crack.
Change made: I used PBKDF2 with SHA-256 to hash passwords. It adds salt and
repeats the hashing process, which makes password guessing harder.
"""

from werkzeug.security import generate_password_hash

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')