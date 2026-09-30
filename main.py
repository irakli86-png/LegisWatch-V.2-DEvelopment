from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# მონაცემთა ბაზის ფუნქციების იმპორტი
from database import (create_table, 
                      insert_bill, 
                      get_bills as get_database_bills, 
                      get_bill_by_id)

from users import create_users_table

# პარლამენტის API-დან მონაცემების ფუნქციის იმპორტი
from api_client import get_bills

# Email ფუნქციის იმპორტი
from email_sender import send_email


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

    