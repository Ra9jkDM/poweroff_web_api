Api for web-angular project
----


# Start

    uvicorn main:app --reload
    http://127.0.0.1:8000/docs


# Gen RSA keys

    openssl genrsa -out private.key 4096
    openssl rsa -in private.key -pubout > public.key
