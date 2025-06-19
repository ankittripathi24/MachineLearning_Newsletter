from html_message_formatter import HTMLMessageFormatter
from send_whatsapp import send_whatsapp_message

def main():
    # Use the new HTML-based formatter instead of the JSON-based one
    formatter = HTMLMessageFormatter()
    message = formatter.get_todays_lesson()
    
    # Send to WhatsApp
    try:
        send_whatsapp_message(message)
        print("Successfully sent message to WhatsApp")
    except Exception as e:
        print(f"Error sending to WhatsApp: {e}")

if __name__ == "__main__":
    main()