from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hasher:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

"""
# Hash a password
hash_pswd = Hasher.get_password_hash("Priyanka")
print("Hashed password:", hash_pswd)

# Verify passwords
print("Verify correct password:", Hasher.verify_password("Priyanka", hash_pswd))  # True
print("Verify wrong password:", Hasher.verify_password("priyanka", hash_pswd))    # False
"""


