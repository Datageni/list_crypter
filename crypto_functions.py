from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Generate an elliptic curve key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Serialize the public key to send to the recipient
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Encryption function
def encrypt_message(public_key, message):
    # Generate an ephemeral key pair
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # Perform key exchange to get a shared secret
    shared_secret = ephemeral_private_key.exchange(ec.ECDH(), public_key)

    # Derive a symmetric key from the shared secret
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_secret)

    # Encrypt the message using AES-GCM
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv)
    ).encryptor()

    ciphertext = encryptor.update(message) + encryptor.finalize()

    return ephemeral_public_key.public_bytes(
               encoding=serialization.Encoding.PEM,
               format=serialization.PublicFormat.SubjectPublicKeyInfo
           ), iv, encryptor.tag, ciphertext

# Decryption function
def decrypt_message(private_key, ephemeral_public_bytes, iv, tag, ciphertext):
    # Load the ephemeral public key
    ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_bytes)

    # Perform key exchange to get the shared secret
    shared_secret = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    # Derive the symmetric key from the shared secret
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_secret)

    # Decrypt the message using AES-GCM
    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag)
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()

# Example usage
message = b"Hello, this is a secret message."

# Encrypt the message
ephemeral_public_bytes, iv, tag, ciphertext = encrypt_message(public_key, message)
print(f"Ciphertext: {ciphertext}")

# Decrypt the message
decrypted_message = decrypt_message(private_key, ephemeral_public_bytes, iv, tag, ciphertext)
print(f"Decrypted message: {decrypted_message}")
