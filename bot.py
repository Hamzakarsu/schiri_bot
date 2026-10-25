import time
import requests
from bs4 import BeautifulSoup

# TELEGRAM BİLGİLERİNİZ
BOT_TOKEN = "8720640821:AAH8beWCYuhJ2UQ2duV203TGgoVUHb-9jCg"
CHAT_ID = "7378245477"

# OFV Hakemsiz Maçlar Sayfası
URL = "https://www.ofv.swiss/ostschweizer-fussballverband/schiedsrichterin-ofv/spiele-ohne-sr-sra-ofv.aspx"

sent_matches = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def check_matches():
    print("Maçlar kontrol ediliyor...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)
        
        if response.status_code != 200:
            print(f"Siteye ulaşılamadı. Kod: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        
        if not tables:
            print("Sayfada tablo bulunamadı.")
            return
            
        new_matches_found = 0
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                text = row.get_text(strip=True)
                if len(text) > 20 and text not in sent_matches:
                    if len(sent_matches) > 0:
                        message = f"🚨 **Yeni Boşta Maç (OFV)!** 🚨\n\n{text}"
                        send_telegram_message(message)
                        new_matches_found += 1
                    sent_matches.add(text)
                    
        print(f"Kontrol tamamlandı. Yeni eklenen maç sayısı: {new_matches_found}")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    print("Bot başlatıldı, OFV maçları takip ediliyor...")
    check_matches()
    
    while True:
        time.sleep(180) # 3 dakika bekle
        check_matches()
