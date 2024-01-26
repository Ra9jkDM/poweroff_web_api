Api for web-angular project
----


# Start

    source .venv/bin/activate
    export $(cat .env)

    python -m database.model # create db

    uvicorn main:app --reload
    http://127.0.0.1:8000/docs


# Gen keys

    openssl rand -hex 32 # secret_key
    openssl genrsa -out private.key 4096
    openssl rsa -in private.key -pubout > public.key
