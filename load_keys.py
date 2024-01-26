
def load_key(filename: str):
    with open(filename, mode="r") as f:
        return f.read()

def get_public_key():
    return load_key("keys/public.key")

def get_private_key():
    return load_key("keys/private.key")