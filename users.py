from keys import generate_keys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import hashlib

def generate_key_files():
    hashed_pk, pk, sk = generate_keys()
    with open("keys/example2.pem", "wb") as f:
        f.write(sk)

    with open("keys/example_pub2.pem", "wb") as f:
        f.write(pk)

    with open("keys/hashed_pk2.txt", "w") as f:
        f.write(hashed_pk)

def generate_signature(payload, file):
    with open(file, "rb") as f:
        pem_private_key = f.read()

    private_key = serialization.load_pem_private_key(
        pem_private_key, password=None, backend=default_backend()
    )
    signature = private_key.sign(payload.encode())

    return signature

def verify_signature(payload, pk_file, signature):
    with open(pk_file, "rb") as f:
        public_key_data = f.read()

    public_key = serialization.load_pem_public_key(
        public_key_data, backend=default_backend()
    )

    try:
        public_key.verify(signature, payload.encode())
        
    except InvalidSignature:
        return "error: This signature is invalid"

    return True
    
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


