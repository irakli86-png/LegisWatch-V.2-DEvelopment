import os
import requests


# Railway-ის BREVO_API_KEY გარემოს ცვლადიდან
# ვიღებთ Brevo API Key-ს
BREVO_API_KEY = os.getenv("BREVO_API_KEY")


# Railway-ის SENDER_EMAIL გარემოს ცვლადიდან
# ვიღებთ გამომგზავნის email-ს
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


# ვაგზავნით email-ს Brevo API-ის საშუალებით
def send_email(email_subject, email_message, receiver_email):

    # Brevo API-ის მისამართი
    url = "https://api.brevo.com/v3/smtp/email"

    # ვუთითებთ API-სთვის საჭირო headers-ს
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    # ვქმნით email-ის მონაცემებს
    data = {
        "sender": {
            "email": SENDER_EMAIL,
            "name": "LegisWatch"
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": email_subject,
        "textContent": email_message
    }

    # ვაგზავნით POST request-ს Brevo API-ში
    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    # თუ API-მ შეცდომა დააბრუნა,
    # პროგრამა გამოიტანს შესაბამის შეცდომას
    response.raise_for_status()