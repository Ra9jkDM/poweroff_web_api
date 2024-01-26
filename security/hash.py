from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha512_crypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    print(hash_password("pass"))