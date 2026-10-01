import os
import psycopg
from pwdlib import PasswordHash
import secrets
import hashlib
from datetime import datetime, timedelta, timezone

DATABASE_URL = os.getenv("DATABASE_URL")

password_hash = PasswordHash.recommended()


def create_users_table():
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_tokens(
            user_id INTEGER PRIMARY KEY
                REFERENCES users(id) ON DELETE CASCADE,
            token_hash TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_user(email, password):
    hashed_password = password_hash.hash(password)

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (email, password_hash)
        VALUES (%s, %s)
        RETURNING id, email, is_verified, created_at
    """, (
        email,
        hashed_password
    ))

    user = cursor.fetchone()

    conn.commit()
    conn.close()

    return user

def create_verification_token(user_id):
    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO email_verification_tokens (
            user_id,
            token_hash,
            expires_at
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            token_hash = EXCLUDED.token_hash,
            expires_at = EXCLUDED.expires_at,
            created_at = CURRENT_TIMESTAMP
    """, (
        user_id,
        token_hash,
        expires_at
    ))

    conn.commit()
    conn.close()

    return token

def verify_email_token(token):
    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM email_verification_tokens
        WHERE token_hash = %s
        AND expires_at > NOW()
    """, (token_hash,))

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False

    user_id = result[0]

    cursor.execute("""
        UPDATE users
        SET is_verified = TRUE
        WHERE id = %s
    """, (user_id,))

    cursor.execute("""
        DELETE FROM email_verification_tokens
        WHERE user_id = %s
    """, (user_id,))

    conn.commit()
    conn.close()

    return True


def authenticate_user(email, password):
    email = email.strip().lower()

    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email, password_hash, is_verified
        FROM users
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        return None

    if not password_hash.verify(password, user[2]):
        return None

    if not user[3]:
        return "not_verified"

    return {
        "id": user[0],
        "email": user[1],
        "is_verified": user[3]
    }
