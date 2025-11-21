import hashlib

# verifies if the given public key matches the stored hashed public key
def verify_user_pk(file_path, public_key):
    with open(file_path, "rb") as f:
        public_key_data = f.read()

    hashed_pk = hashlib.sha256(public_key_data.encode()).hexdigest()

    if hashed_pk != public_key:
        return False
    return True

# Returns the raw key data from a file
def get_user_key_data(file_path):
    with open(file_path, "rb") as f:
        key_data = f.read()

    return key_data

# Returns the SHA-256 hash of a public key
def hash_pk(pk):
    hashed_pk = hashlib.sha256(pk).hexdigest()
    return hashed_pk

