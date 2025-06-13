import cbor2, hashlib
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography import x509

# ----------------------------------------------------------------------
# 1.  Load and carve out the pieces already in your script
# ----------------------------------------------------------------------
with open("decoded.bin", "rb") as f:
    root = cbor2.load(f)

issuer_auth      = root["issuer_auth"]          # 4-element COSE_Sign1
protected_bstr   = issuer_auth[0]               # bytes
payload_bstr     = issuer_auth[2]               # bytes
signature_bstr   = issuer_auth[3]               # 64 bytes (r‖s)

# Build Sig_structure and hash (not strictly needed for verify())
sig_structure = ["Signature1", protected_bstr, b"", payload_bstr]
sig_bytes     = cbor2.dumps(sig_structure, canonical=True)

# ----------------------------------------------------------------------
# 2.  Turn raw 64-byte (r‖s) into ASN.1 DER for cryptography’s verify()
# ----------------------------------------------------------------------
r = int.from_bytes(signature_bstr[:32], "big")
s = int.from_bytes(signature_bstr[32:], "big")
signature_der = utils.encode_dss_signature(r, s)   # ← key step!

# ----------------------------------------------------------------------
# 3.  Load the issuer certificate and extract its EC-P256 public key
# ----------------------------------------------------------------------
with open("issuance/issuer-cert.pem", "rb") as f:
    issuer_pub = x509.load_pem_x509_certificate(f.read()).public_key()

# ----------------------------------------------------------------------
# 4.  Verify
# ----------------------------------------------------------------------
try:
    issuer_pub.verify(                   # will raise InvalidSignature on failure
        signature_der,
        sig_bytes,                       # the *exact* Sig_structure bytes
        ec.ECDSA(hashes.SHA256()),       # ES256 → ECDSA-P256 + SHA-256
    )
    print("✅  COSE_Sign1 signature is VALID with issuer cert")
except InvalidSignature:
    print("❌  Signature verification FAILED — check cert & CBOR bytes")