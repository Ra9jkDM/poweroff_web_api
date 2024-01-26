from passlib.hash import sha512_crypt

if __name__ == "__main__":
    hash = sha512_crypt.hash("pass")
    print(hash)