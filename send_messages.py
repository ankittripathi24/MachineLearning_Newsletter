import os
from html_message_formatter import HTMLMessageFormatter
from send_whatsapp import send_message

def main():
    # Use the new HTML-based formatter instead of the JSON-based one
    formatter = HTMLMessageFormatter()
    message = formatter.get_todays_lesson()
    
    # Send to WhatsApp
    try:
        send_message(message)
        print("Successfully sent message to WhatsApp")
        
        # Output the message for workflow systems to capture
        if "GITHUB_OUTPUT" in os.environ:
            # For GitHub Actions
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                # Properly escape the message for GitHub Actions output
                escaped_message = message.replace("%", "%25").replace("\n", "%0A").replace("\r", "%0D")
                f.write(f"summary={escaped_message}\n")
        else:
            # For other workflow systems or local testing
            print(f"::set-output name=summary::{message}")
            
    except Exception as e:
        print(f"Error sending to WhatsApp: {e}")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"summary=Error: {str(e)}\n")
        else:
            print(f"::set-output name=summary::Error: {str(e)}")

if __name__ == "__main__":
    main()