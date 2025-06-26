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

print(len(sig_bytes))

# ----------------------------------------------------------------------
# 2.  Turn raw 64-byte (r‖s) into ASN.1 DER for cryptography’s verify()
# ----------------------------------------------------------------------
r = int.from_bytes(signature_bstr[:32], "big")
s = int.from_bytes(signature_bstr[32:], "big")
signature_der = utils.encode_dss_signature(r, s)   # ← key step!


print(signature_der)
print(signature_bstr)

# ----------------------------------------------------------------------
# 3.  Load the issuer certificate and extract its EC-P256 public key
# ----------------------------------------------------------------------
with open("issuance/issuer-cert.pem", "rb") as f:
    issuer_pub = x509.load_pem_x509_certificate(f.read()).public_key()

# ----------------------------------------------------------------------
# 4.  Verify
# ----------------------------------------------------------------------
# try:
#     issuer_pub.verify(                   # will raise InvalidSignature on failure
#         signature_der,
#         sig_bytes,                       # the *exact* Sig_structure bytes
#         ec.ECDSA(hashes.SHA256()),       # ES256 → ECDSA-P256 + SHA-256
#     )
#     print("✅  COSE_Sign1 signature is VALID with issuer cert")
# except InvalidSignature:
#     print("❌  Signature verification FAILED — check cert & CBOR bytes")


from tinyec import ec, registry
import hashlib
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization

curve = registry.get_curve("secp256r1")
n     = curve.field.n

# --- public key point -------------------------------------------------
sec1 = issuer_pub.public_bytes(
    serialization.Encoding.X962,
    serialization.PublicFormat.UncompressedPoint,
)
#print(sec1)

Q = ec.Point(curve,
             int.from_bytes(sec1[1:33], "big"),   # x
             int.from_bytes(sec1[33:],  "big"))   # y

# --- signature & hash -------------------------------------------------
r = int.from_bytes(signature_bstr[:32], "big")
s = int.from_bytes(signature_bstr[32:], "big")
if not (1 <= r < n and 1 <= s < n):               # range check
    raise ValueError("Bad r/s")

e = int.from_bytes(hashlib.sha256(sig_bytes).digest(), "big") % n

# --- classic ECDSA verify --------------------------------------------
w  = pow(s, -1, n)
u1 = (e * w) % n
u2 = (r * w) % n
P  = u1 * curve.g + u2 * Q                       # point add & mul
valid = (P.x % n) == r


print("✅" if valid else "❌", "signature is", "valid" if valid else "invalid")