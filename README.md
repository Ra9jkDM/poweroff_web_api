Api for web-angular project
----
It is server template, that works with access and refresh jwt tokens.

To store data it uses SQLAlchemy ORM(```database/model.py```). ```database/tables/*``` - this files needed to perform actions with tables like as CREATE/SELECT/UPDATE/DELETE. File names and table names are the same. ```@session``` decorator needed to open session.

```business_login/database/tables/*``` needed for preprocessing and convert data to ```pydantic``` like types. All ```pydantic``` like types create in ```business_login/database/model_dto.py```. Convert expressions are stored in ```business_login/database/converter.py```.

In folder ```routers``` are stored FastAPI routers.

In folder ```security``` are stored files related with JWT tokens.

All routes are registered in ```main.py```/

# Start

    source .venv/bin/activate
    pip install -m requirements.txt
    export $(cat .env)

    python -m database.model # create db

    uvicorn main:app --reload
    # http://127.0.0.1:8000/docs


# Gen keys

    openssl rand -hex 32 # secret_key (set value in .env file in 'secret_key=')

    # copy keys to 'security/keys'
    openssl genrsa -out private.key 4096
    openssl rsa -in private.key -pubout > public.key


# Change lifetime for JWT tokens

Change values to variables: ```ACCESS_TOKEN_EXPIRE_MINUTES``` and ```REFRESH_TOKEN_EXPIRE_MINUTES```
in file ```security/jwt.py```