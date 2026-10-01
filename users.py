import os
import psycopg
from pwdlib import PasswordHash

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