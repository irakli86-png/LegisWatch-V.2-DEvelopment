        
import requests

# ეს არის პარლამენტის API ის მისამართი საიდანაც ვიღებთ ინფორმაციას
url = "https://info.parliament.ge/law/1/bill"


# ეს ფუნქცია იღებს დოკუმენტებს პარლამენტის API დან
def get_bills():

    headers = {
        "User-Agent": "Mozilla/5.0" #აქ ვუთითებთ, რომ HTTP ის მოთხოვნა ბრაუზერის მსგავსად იგზავნება
    }

    filtered_bills = [] # ვქმნით ცარიელ ცვლადს ლისტის სახით რომ შემდგომ დავამატოთ გაფილტრული დოკუმენტები
# აქ მითითებული მაქვს API ის მოთხოვნის პარამეტრები: რომელი ჩანაწერიდან ვიწყებთ და რამდენ ჩანაწერს ვღებულობთ
# API-ს ვთხოვთ მონაცემებს 3 გვერდად, თითო გვერდზე 25 ჩანაწერით
# start განსაზღვრავს, რომელი ჩანაწერიდან იწყება თითოეული გვერდი
    for start in [0, 25, 50]:
        params = {
            "start": start,
            "limit": 25
        }
        try:
# ამით მოთხოვნას ვაგზავნით
            response = requests.get(url, headers=headers, params=params, timeout=10)

            response.raise_for_status()

        except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError
        ):
            print("API-სთან დაკავშირებისას პრობლემა მოხდა")
            continue

# პირველი ფილტრი, თუ მოთხოვნა წარმატებულია 
        if response.status_code == 200:

            data = response.json()
# აქ ლუპის მეშვეობით ვაკეთებთ მეორე ფილტრებს რათა პარლამენტიუს საიტიდან მხოლოდ კანონპროექტები და ორგანული
#კანონის პროექტები წამოვიღოთ
            for bill in data["list"]:
                if bill["billType"]["id"] == 1 or bill["billType"]["id"] == 11:
                    filtered_bills.append(bill)
                
    return filtered_bills        
                
# აქ კი ლისტის სახით ვაბრუნებთ
      
