import os
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Lib.Debugger import info
def generate_self_signed_cert(cert_path="Server/Data/Certs/server.crt", key_path="Server/Data/Certs/server.key"):
    if os.path.exists(cert_path) and os.path.exists(key_path):
        return
    info("Generating self-signed certificate for TLS pinning...")
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CodeFurnace"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"codefurnace.c2"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    info(f"Certificate generated at {cert_path}")
    
    import shutil
    rust_client_cert = "Client/Payloads/Rust/reverse_shell/src/server.crt"
    if os.path.exists("Client/Payloads/Rust/reverse_shell/src"):
        shutil.copy(cert_path, rust_client_cert)
        info(f"Certificate copied to {rust_client_cert}")
if __name__ == "__main__":
    generate_self_signed_cert()
