import os
import re
import smtplib
import time
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE")
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def get_url_and_warnings():
    """URLとWARNINGをログから取得"""
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    url = None
    warnings = []

    for line in lines:
        if not url:
            match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", line)
            if match:
                url = match.group(0)
        if "WARNING" in line:
            warnings.append(line.strip())

    return url, warnings


def send_email(url, warnings, timeout=False):
    """メール送信処理"""
    if timeout:
        body = "Timeout occurred while trying to retrieve the Streamlit App URL."
    else:
        body = f"New Streamlit App URL: {url}"
        if warnings:
            body += "\n\nWarnings:\n" + "\n".join(warnings)

    msg = MIMEText(body)
    msg["Subject"] = "research-project-processing App URL"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)


def wait_for_log(timeout=60):
    """ログが空でなくなるまで待機"""
    for _ in range(timeout):
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            return True
        time.sleep(1)
    return False


def main():
    if not wait_for_log():
        print("Log file did not update in time.")
        send_email(None, [], timeout=True)  # Timeoutメールを送信
        return

    url = None
    warnings = []
    for _ in range(30):  # 最大30回試行（30秒）
        url, warnings = get_url_and_warnings()
        if url:
            send_email(url, warnings)
            print(f"Sent URL: {url}")
            return
        time.sleep(1)

    print("URL not found within timeout.")
    send_email(None, [], timeout=True)  # Timeoutメールを送信


if __name__ == "__main__":
    main()
