from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# მონაცემთა ბაზის ფუნქციების იმპორტი
from database import (create_table, 
                      insert_bill, 
                      get_bills as get_database_bills, 
                      get_bill_by_id)

from users import (
    create_users_table,
    create_user,
    create_verification_token,
    verify_email_token,
    authenticate_user
)

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# პარლამენტის API-დან მონაცემების ფუნქციის იმპორტი
from api_client import get_bills

# Email ფუნქციის იმპორტი
from email_sender import send_email
import os
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return {
            "id": int(user_id),
            "email": payload.get("email")
        }

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )



# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(title="LegisWatch")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "https://front-end-production-e71d.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()
create_users_table()
# მთავარი გვერდი
@app.get("/")
def home():
    return {
        "message": "LegisWatch is running"
    }


@app.post("/register")
def register(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    if not isinstance(email, str) or not isinstance(password, str):
        raise HTTPException(
            status_code=400,
            detail="Email and password must be strings"
        )

    email = email.strip().lower()

    if not email or len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password must be at least 8 characters"
        )

    try:
        user = create_user(email, password)

    except Exception as error:
        if "duplicate key" in str(error):
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

    token = create_verification_token(user[0])

    verification_link = (
        "https://legiswatch-v2-development-production.up.railway.app"
        f"/verify-email?token={token}"
    )

    email_subject = "Verify your LegisWatch account"

    email_message = (
        "Welcome to LegisWatch!\n\n"
        "Please verify your email address by opening this link:\n\n"
        f"{verification_link}\n\n"
        "This link expires in 24 hours."
    )

    try:
        send_email(
            email_subject,
            email_message,
            email
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail=(
                "Account created, but verification email could not "
                "be sent. Please contact support."
            )
        )

    return {
        "message": "Registration successful. Please verify your email.",
        "user": {
            "id": user[0],
            "email": user[1],
            "is_verified": user[2],
            "created_at": user[3]
        }
    }


@app.get("/verify-email")
def verify_email(token: str):
    is_verified = verify_email_token(token)

    if not is_verified:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification token"
        )

    return {
        "message": "Email verified successfully"
    }



@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    if not isinstance(email, str) or not isinstance(password, str):
        raise HTTPException(
            status_code=400,
            detail="Email and password must be strings"
        )

    user = authenticate_user(email, password)

    if user == "not_verified":
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first"
        )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Authentication is not configured"
        )

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }


@app.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Authenticated successfully",
        "user": current_user
    }


@app.get("/bills")
def bills(limit: int = 10, offset: int = 0, search: str = ""):

    # ბაზიდან მოგვაქვს ყველა ინიციატივა
    result = get_database_bills(limit, offset, search)

    # ვაბრუნებთ მიღებულ მონაცემებს
    return result

@app.get("/bills/{bill_id}")
def bill(bill_id):

    # ბაზიდან მოგვაქვს კონკრეტული ინიციატივა
    result = get_bill_by_id(bill_id)
     # თუ ასეთი ინიციატივა ვერ მოიძებნა
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="დოკუმენტი ვერ მოიძებნა"
        )

       # ვაბრუნებთ ინიციატივას
    return result

# დაემატა ახალი -----------

@app.get("/run")
def run():

    run_legiswatch()

    return {
        "message": "LegisWatch run completed"
    }

@app.post("/check-updates")
def check_updates(data: dict):

    email = data.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    new_bills_count = run_legiswatch(email)

    return {
        "message": "Updates checked successfully",
        "new_bills": new_bills_count
    }

# --------------------------------------------------
# LegisWatch-ის ავტომატიზაციის ფუნქცია
# --------------------------------------------------

def run_legiswatch(receiver_email="irakli.ivanidze86@gmail.com"):

    # ცხრილის შექმნა
    create_table()

    # API-დან მონაცემების მიღება
    bills = get_bills()

    # სია, სადაც შევინახავთ მხოლოდ ახალ კანონპროექტებს
    new_bills = []

    # Email-ზე გასაგზავნი ტექსტი
    email_message = ""

    # მიღებული კანონპროექტების ციკლით დამუშავება
    for option in bills:

        # მონაცემთა ბაზაში დამატება
        was_saved = insert_bill(option)

        # თუ ახალი კანონპროექტია
        if was_saved:
            new_bills.append(option)

    # Email-ის სათაური
    email_message += (
        f"ნაპოვნია {len(new_bills)} ახალი საკანონმდებლო ინიციატივა.\n\n"
    )

    # დანომრილი კანონპროექტების ჩამონათვალი
    for number, option in enumerate(new_bills, start=1):

        email_message += (
            f"{number}. {option['billName']}\n"
        )

        # კონკრეტული კანონპროექტის ბმული
        email_message += (
            f"https://info.parliament.ge/#law-drafting/"
            f"{option['id']}\n\n"
        )

    # Email-ის მონაცემები
    email_subject = (
        "მოგესალმებათ LegisWatch - ახალი საკანონმდებლო ინიციატივები"
    )

    send_email(
    email_subject,
    email_message,
    receiver_email
)

    return len(new_bills)

# --------------------------------------------------
# თუ ფაილს პირდაპირ Python-ით გავუშვებთ
# --------------------------------------------------

if __name__ == "__main__":
    run_legiswatch()

    