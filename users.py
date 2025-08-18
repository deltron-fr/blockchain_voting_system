from ecdsa import SigningKey, NIST256p

users_info = [
    {
        "user_sk": """-----BEGIN PRIVATE KEY-----
                      MIGHAgEBMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgz5S0uQJQnIUx8Txt0ClsoCkU5knV
                      5p610ck0dKVureShRANCAASBy/f/Hotqd1uGaVr4foEEwp2eXQL8K62GlD9MG5j6UZDMW6vnlD4T
                      5qCzcun8epCOvIJxumFx7RJUoW3C/MfF
                      -----END PRIVATE KEY-----""",
        "user_pk": """-----BEGIN PUBLIC KEY-----
                      MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEgcv3/x6Landbhmla+H6BBMKdnl0C/CuthpQ/TBuY
                      +lGQzFur55Q+E+ags3Lp/HqQjryCcbphce0SVKFtwvzHxQ==
                      -----END PUBLIC KEY-----"""
    }
]


private_key = SigningKey.generate(curve=NIST256p)
print(private_key)
public_key = private_key.verifying_key