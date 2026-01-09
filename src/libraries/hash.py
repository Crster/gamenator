import hashlib
import secrets


def generate_random_sha256():
    # Generate 32 cryptographically secure random bytes (256 bits)
    # 32 bytes is the recommended default for secure tokens
    random_bytes = secrets.token_bytes(32)

    # Create a new SHA256 hash object
    hash_object = hashlib.sha256()

    # Feed the random bytes to the hash object
    hash_object.update(random_bytes)

    # Return the hash as a hexadecimal string
    return hash_object.hexdigest()
