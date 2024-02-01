Api for web-angular project
----
It is server template, that works with access and refresh jwt tokens.

To store data it uses SQLAlchemy ORM(```database/model.py```). ```database/tables/*``` - this files needed to perform actions with tables like as CREATE/SELECT/UPDATE/DELETE. File names and table names are the same. ```@session``` decorator needed to open session.

```business_login/database/tables/*``` needed for preprocessing and convert data to ```pydantic``` like types. All ```pydantic``` like types create in ```business_login/database/model_dto.py```. Convert expressions are stored in ```business_login/database/converter.py```.

In folder ```routers``` are stored FastAPI routers.

In folder ```security``` are stored files related with JWT tokens.

All routes are registered in ```main.py```/

# Start

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    export $(cat .env)

    python -m database.model # create db

    uvicorn main:app --reload
    # http://127.0.0.1:8000/docs

Default user: <br>
Login: **bob**<br>
Password: **pwd123**

Can change login and password in ```database/model.py```(create_user("LOGIN", "PASSWORD")) file, before creating db.


# Gen keys

    openssl rand -hex 32 # secret_key (set value in .env file in 'secret_key=')

    # copy keys to 'security/keys'
    openssl genrsa -out private.key 4096
    openssl rsa -in private.key -pubout > public.key


# Change lifetime for JWT tokens

Change values to variables: ```ACCESS_TOKEN_EXPIRE_MINUTES``` and ```REFRESH_TOKEN_EXPIRE_MINUTES```
in file ```security/jwt.py```

# Allow CORS

> Cross-Origin Resource Sharing

To allow requests from hosts, add necessary host in ```main.py``` in **origins** array:

    origins = [
        "http://localhost:4200",
        "http://localhost:8080",
    ]

And allow request in **Nginx**:

    server {
        listen 4010      ssl http2;
        listen [::]:4010 ssl http2;
        server_name _;

        client_max_body_size 100M;

        ssl_certificate /etc/letsencrypt/live/<SITE>/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/<SITE>/privkey.pem; # managed by Certbot
    #    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        # web_api
        location / {
            if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            #
            # Custom headers and headers various browsers *should* be OK with but aren't
            #
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
            #
            # Tell client that this pre-flight info is valid for 20 days
            #
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        if ($request_method = 'POST') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
            add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        }
        if ($request_method = 'GET') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
            add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        }


            proxy_pass http://localhost:4011/; # URL where the api is running

            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

    }

# Create user and grant access on db in PostgreSQL


Warning: Do **NOT** use these commands in production

    CREATE DATABASE <DB>;
    CREATE USER <USER> WITH PASSWORD '<PASSWORD>';
    GRANT CONNECT ON DATABASE <DB> TO <USER>;
    GRANT ALL ON DATABASE <DB> TO <USER>;
    GRANT ALL ON SCHEMA public TO <USER>;