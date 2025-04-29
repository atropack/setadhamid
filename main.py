import requests
from bs4 import BeautifulSoup
import telegram
import os

TELEGRAM_TOKEN = os.getenv("7850841863:AAFLaoKxUhylBr7q5J8F_lIMg0JHF9gIOuQ
")
CHANNEL_ID = os.getenv("SETADHAMID")

def send_to_telegram(tenders):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    if not tenders:
        return

    message = "📢 *مناقصات امروز:*\n\n"
    for tender in tenders:
        message += "━━━━━━━━━━━━━━━━━━\n"
        message += f"🔹 *کد آگهی:* `{tender['code']}`\n"
        message += f"📌 *عنوان:* {tender['title']}\n"
        message += f"🏙️ *شهر:* {tender['city']}\n"
        message += f"⏰ *مهلت:* {tender['deadline']}\n"
    message += "━━━━━━━━━━━━━━━━━━"

    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")

def scrape_tenders():
    url = "https://setadiran.ir/setad/cms/tender"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tenders = []
    for item in soup.select(".tender-item")[:5]:  # (نیاز به تطبیق دقیق تر با HTML واقعی داره)
        tenders.append({
            "code": item.select_one(".code").text.strip(),
            "title": item.select_one(".title").text.strip(),
            "city": item.select_one(".city").text.strip(),
            "deadline": item.select_one(".deadline").text.strip(),
        })

    send_to_telegram(tenders)

if __name__ == "__main__":
    scrape_tenders()
