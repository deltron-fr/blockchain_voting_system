from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import hashlib

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

