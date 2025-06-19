from message_formatter import MessageFormatter

from send_whatsapp import send_whatsapp_message

def main():
    formatter = MessageFormatter()
    message = formatter.get_todays_lesson()
    
    # Send to WhatsApp
    try:
        send_whatsapp_message(message)
        print("Successfully sent message to WhatsApp")
    except Exception as e:
        print(f"Error sending to WhatsApp: {e}")

if __name__ == "__main__":
    main()