#hashing logic to assure minimal database security

from passlib.context import CryptContext
hash_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(string_to_hash: str) -> str:
    return hash_context.hash(string_to_hash)

def verify(plain_password: str, password: str):
    return hash_context.verify(plain_password, password)