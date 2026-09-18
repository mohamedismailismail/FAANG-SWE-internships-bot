import requests    # Used for speaking to Telegram APIs(Application programming interfaces)
from config import BOT_TOKEN, CHAT_ID    # Import the sensitive Data from config.py

def send_telegram_alert(message: str) -> bool:    # Function recieves str and out boolean value
    """
    Sends a formatted Markdown message to the configured Telegram chat.
    Returns True if sent successfully, False otherwise.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",    # *Bold*, `code`
        "disable_web_page_preview": False    # Make clicking on the link easy
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        # json ==> The universal data format that all language connect with each other throug APIs 
        response.raise_for_status()
        print(">> Message delivered successfully to Telegram!")
        return True
    except requests.exceptions.RequestException as error:
        print(f">> Failed to send message: {error}")
        return False

if __name__ == "__main__":    # used in testing the bot only
    # Test alert
    test_message = (
        "*FAANG Alerts Bot Initialized!🔥*\n\n"
        "Testing Telegram integration for upcoming SWE Internships.\n"
        "Status: `Online & Ready`"
    )
    send_telegram_alert(test_message)