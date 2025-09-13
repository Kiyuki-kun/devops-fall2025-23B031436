from flask import Flask, request, jsonify, abort
import os
import psycopg2
import psycopg2.extras
import datetime
import hashlib
import secrets

DB_DSN = os.environ.get("DATABASE_URL", "postgresql://vagrant:password@127.0.0.1/simpleauth")
TOKEN_TTL_SECONDS = 2 * 3600  # 2 hours

app = Flask(__name__)

def get_db():
    return psycopg2.connect(DB_DSN, cursor_factory=psycopg2.extras.RealDictCursor)

def generate_token():
    # strong random token
    return secrets.token_urlsafe(32)

@app.route("/token", methods=["POST"])
def token():
    # Expect form data: grant_type=client_credentials, client_id, client_secret, scope (space separated)
    grant_type = request.form.get("grant_type", "")
    client_id = request.form.get("client_id", "")
    client_secret = request.form.get("client_secret", "")
    scope = request.form.get("scope", "")

    if grant_type != "client_credentials":
        return jsonify({"error": "unsupported_grant_type"}), 400
    if not (client_id and client_secret):
        return jsonify({"error": "invalid_client"}), 400

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT client_id, client_secret, scope FROM public.app_client WHERE client_id = %s", (client_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "invalid_client"}), 401
            if row["client_secret"] != client_secret:
                return jsonify({"error": "invalid_client"}), 401

            allowed_scopes = row["scope"] or []
            requested = scope.split()
            # check requested scopes are subset of allowed
            if requested and not set(requested).issubset(set(allowed_scopes)):
                return jsonify({"error": "invalid_scope"}), 400

            # generate token and persist minimal data
            access_token = generate_token()
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_TTL_SECONDS)
            # Store only client_id, token, scopes array, expiration timestamp
            cur.execute(
                "INSERT INTO public.token (client_id, access_scope, access_token, expiration_time) VALUES (%s, %s, %s, %s)",
                (client_id, requested or allowed_scopes, access_token, expires_at)
            )
            conn.commit()

            resp = {
                "access_token": access_token,
                "expires_in": TOKEN_TTL_SECONDS,
                "refresh_token": "",
                "scope": " ".join(requested or allowed_scopes),
                "security_level": "normal",
                "token_type": "Bearer"
            }
            return jsonify(resp), 200

@app.route("/check", methods=["GET"])
def check():
    # expects Authorization: Bearer <token>
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing_token"}), 401
    access_token = auth.split(None, 1)[1].strip()

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT client_id, access_scope, expiration_time FROM public.token WHERE access_token = %s", (access_token,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "invalid_token"}), 401
            if row["expiration_time"] < datetime.datetime.utcnow():
                return jsonify({"error": "expired_token"}), 401

            return jsonify({"ClientID": row["client_id"], "Scope": " ".join(row["access_scope"] or [])}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))