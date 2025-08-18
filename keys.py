from ecdsa import SigningKey, NIST256p

private_key = SigningKey.generate(curve=NIST256p)
with open("sk.pem", "wb") as f:
    f.write(private_key.to_pem(format="pkcs8"))

public_key = private_key.verifying_key
with open("pub_key.pem", "wb") as f:
    f.write(public_key.to_pem())