import os
import psycopg
from psycopg.rows import dict_row


# Railway-ის DATABASE_URL გარემოს ცვლადიდან
# ვიღებთ PostgreSQL-ის მონაცემებს
DATABASE_URL = os.getenv("DATABASE_URL")


# ვქმნით bills ცხრილს, თუ ის ჯერ არ არსებობს
def create_table():

    # ვუკავშირდებით PostgreSQL მონაცემთა ბაზას
    conn = psycopg.connect(DATABASE_URL)

    # ვქმნით cursor-ს SQL ბრძანებების შესასრულებლად
    cursor = conn.cursor()
    
    # ვქმნით bills ცხრილს
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills(
        id SERIAL PRIMARY KEY,
        bill_id INTEGER UNIQUE,
        bill_name TEXT,
        bill_description TEXT,
        bill_type TEXT,
        registration_number TEXT,
        registration_date TEXT,
        package_name TEXT,
        initiator TEXT,
        author TEXT,
        bill_count INTEGER,
        confirmed_procedure BOOLEAN
        )
    """)

    # ვინახავთ ცვლილებას მონაცემთა ბაზაში
    conn.commit()

    # ვხურავთ კავშირს მონაცემთა ბაზასთან
    conn.close()


# ვამოწმებთ, არსებობს თუ არა კონკრეტული bill_id მონაცემთა ბაზაში
def bill_exists(bill_id):

    # ვუკავშირდებით PostgreSQL მონაცემთა ბაზას
    conn = psycopg.connect(DATABASE_URL)

    # ვქმნით cursor-ს
    cursor = conn.cursor()

    # ვეძებთ კონკრეტულ bill_id-ს bills ცხრილში
    cursor.execute(
        "SELECT * FROM bills WHERE bill_id = %s",
        (bill_id,)
    )

    # ვიღებთ ნაპოვნ პირველ ჩანაწერს
    result = cursor.fetchone()

    # ვხურავთ კავშირს
    conn.close()

    # თუ ჩანაწერი ვერ ვიპოვეთ
    if result is None:
        return False

    # თუ ჩანაწერი არსებობს
    else:
        return True


# ვამატებთ ახალ საკანონმდებლო ინიციატივას მონაცემთა ბაზაში
def insert_bill(bill):
    # API-დან მიღებული bill dictionary-დან
    # ვიღებთ bill-ის ID-ს
    bill_id = bill["id"]

    # API-დან მიღებული bill dictionary-დან
    # ვიღებთ bill-ის სახელს
    bill_name = bill["billName"]

    bill_description = bill["billDescription"]
    bill_type = bill["billType"]["name"]
    registration_number = bill["billPackage"]["registrationNumber"]
    registration_date = bill["billPackage"]["registrationDate"]
    package_name = bill["billPackage"]["packageName"]
    initiator = bill["billPackage"]["initiator"]
    author = bill["billPackage"]["author"]
    bill_count = bill["billPackage"]["billCount"]
    confirmed_procedure = bill["billPackage"]["confirmedProcedure"]

    # ჯერ ვამოწმებთ, ხომ არ არსებობს ეს ინიციატივა
    if not bill_exists(bill_id):

        # ვუკავშირდებით PostgreSQL მონაცემთა ბაზას
        conn = psycopg.connect(DATABASE_URL)

        # ვქმნით cursor-ს
        cursor = conn.cursor()

        # ვამატებთ ახალ ჩანაწერს bills ცხრილში
        cursor.execute("""
    INSERT INTO bills (
        bill_id,
        bill_name,
        bill_description,
        bill_type,
        registration_number,
        registration_date,
        package_name,
        initiator,
        author,
        bill_count,
        confirmed_procedure
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
""", (
    bill_id,
    bill_name,
    bill_description,
    bill_type,
    registration_number,
    registration_date,
    package_name,
    initiator,
    author,
    bill_count,
    confirmed_procedure
))

        # ვინახავთ ცვლილებას მონაცემთა ბაზაში
        conn.commit()

        # ვხურავთ კავშირს
        conn.close()

        # ვატყობინებთ main.py-ს,
        # რომ ახალი ინიციატივა ნამდვილად დაემატა
        return True

    # თუ bill_id უკვე არსებობდა
    else:

        # ვატყობინებთ main.py-ს,
        # რომ ახალი ჩანაწერი არ დამატებულა
        return False

def get_bills(limit,offset, search):

    # ვუკავშირდებით PostgreSQL მონაცემთა ბაზას
    
    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )
    # ვქმნით cursor-ს
    cursor = conn.cursor()

   
    # მოგვაქვს bills ცხრილში არსებული ყველა ჩანაწერი
    cursor.execute("""
    SELECT *
    FROM bills
    WHERE bill_name ILIKE %s
    LIMIT %s
    OFFSET %s
""", (f"%{search}%", limit, offset))

    # ვინახავთ ყველა ჩანაწერს
    bills = cursor.fetchall()

    # ვხურავთ კავშირს
    conn.close()

    return bills

def get_bill_by_id(bill_id):

    # ვუკავშირდებით PostgreSQL მონაცემთა ბაზას
    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

    # ვქმნით cursor-ს
    cursor = conn.cursor()

    # ვეძებთ კონკრეტულ bill_id-ს
    cursor.execute(
        """
        SELECT *
        FROM bills
        WHERE bill_id = %s
        """,
        (bill_id,)
    )

    # ვიღებთ ნაპოვნ ჩანაწერს
    bill = cursor.fetchone()

    # ვხურავთ კავშირს
    conn.close()

    return bill