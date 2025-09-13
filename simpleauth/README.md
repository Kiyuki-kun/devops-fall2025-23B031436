# SimpleAuth - pseudo-OAuth API

Small demo OAuth2-like service with two endpoints:
- POST /token  -> issues access token (grant_type=client_credentials)
- GET /check   -> validates token (Authorization: Bearer <token>)

Features:
- Tokens valid for 2 hours
- Minimal token table (client_id, access_scope array, token, expiration)
- PostgreSQL for storage
- Runs inside Vagrant VM and can be managed via systemd (unit provided)

## Quick start (local)
1. Install PostgreSQL and Python 3.8+
2. Create a DB and run `migrations/init.sql`
3. Create a virtualenv, `pip install -r requirements.txt`
4. Export `DATABASE_URL` env var and run `python app.py` or use gunicorn for production.

## Vagrant
Run `vagrant up` in the repository root to provision an Ubuntu VM that installs dependencies,
initializes the DB and runs the app as a systemd service.

## Security notes
- Do NOT store secrets in code for production. Use environment variables or a secrets manager.
- Use proper password hashing/salting (bcrypt/argon2) for client_secret storage.
- Use TLS in production.