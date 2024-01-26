import database.tables.refresh_token as refresh_token
import business_logic.database.converter as convert


def save(user_id: int, token: str):
    refresh_token.save(user_id, token)

def delete(token: str):
    refresh_token.delete(token)

def delete_many(tokens: list[int]):
    return refresh_token.delete_many(tokens)

def is_active(user_id: str, token: str):
    token = refresh_token.get(int(user_id), token)

    if token:
        return True
    return False

def get_all(user_id: int):
    return refresh_token.get_all(user_id)

def get_all_for_user(user_id: int, current_token: str):
    tokens = refresh_token.get_all(user_id)
    
    result = []

    for i in tokens:
        token = convert.refresh_token(i)
        if i.token == current_token:
            token.current=True

        result.append(token)
    
    result = sorted(result, key=lambda x: x.id)

    return result