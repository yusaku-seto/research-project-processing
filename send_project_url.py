import os
import re
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()

LOG_FILE = os.getenv("LOG_FILE")
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def get_url_from_log():
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    for line in reversed(lines):
        match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", line)
        if match:
            return match.group(0)
    return None


def send_email(url):
    msg = MIMEText(f"New Streamlit App URL: {url}")
    msg["Subject"] = "research-project-processing App URL"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)


def main():
    url = get_url_from_log()
    if url:
        send_email(url)
        print(f"Sent URL: {url}")
    else:
        print("No URL found in log.")


if __name__ == "__main__":
    main()
