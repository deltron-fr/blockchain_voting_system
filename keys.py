from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import hashlib
from utils import serialize_payload

# Generates a new Ed25519 key pair and returns the hashed public key, public key, and private key
def generate_keys():
    private_key = Ed25519PrivateKey.generate()

    public_key = private_key.public_key()

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    hashed_pk = hashlib.sha256(pem_public_key).hexdigest()

    return hashed_pk, pem_public_key, pem_private_key


def generate_key_files():
    hashed_pk, pk, sk = generate_keys()
    with open("keys/exam5.pem", "wb") as f:
        f.write(sk)

    with open("keys/exam5_pub.pem", "wb") as f:
        f.write(pk)

    with open("keys/hashed_pk5.txt", "w") as f:
        f.write(hashed_pk)

# Generates a signature for the given payload using the private key from the specified file
def generate_signature(payload, file):
    with open(file, "rb") as f:
        pem_private_key = f.read()

    private_key = serialization.load_pem_private_key(
        pem_private_key, password=None, backend=default_backend()
    )

    data = serialize_payload(payload)
    signature = private_key.sign(data)

    return signature.hex()

def verify_signature(payload, pk_data, signature):

    public_key = serialization.load_pem_public_key(
        pk_data, backend=default_backend()
    )

    data = serialize_payload(payload)
    try:
        public_key.verify(bytes.fromhex(signature), data)
        
    except InvalidSignature:
        return False

    return True

