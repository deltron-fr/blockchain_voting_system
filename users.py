from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import hashlib

def verify_user_pk(file_path, public_key):
    with open(file_path, "rb") as f:
        public_key_data = f.read()

    public_key = serialization.load_pem_public_key(
        public_key_data, backend=default_backend()
    )

    hashed_pk = hashlib.sha256(public_key.encode()).hexdigest()

    if hashed_pk != public_key:
        return False
    return True

def get_user_key_data(file_path):
    with open(file_path, "rb") as f:
        key_data = f.read()

    return key_data

def hash_pk(pk):
    hashed_pk = hashlib.sha256(pk).hexdigest()
    return hashed_pk

