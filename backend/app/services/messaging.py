import firebase_admin
from firebase_admin import messaging
from typing import Optional

def send_push_notification(
    token: str, 
    title: str, 
    body: str, 
    data: Optional[dict] = None,
    priority: str = "normal"
):
    """
    Sends a standard Firebase Cloud Message to a specific device.
    """
    if not token:
        print("Error: No FCM token provided for notification.")
        return

    try:
        # Construct the message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=token,
            # Android specific config for priority
            android=messaging.AndroidConfig(
                priority="high" if priority == "high" else "normal",
                notification=messaging.AndroidNotification(
                    icon="stock_ticker_update",
                    color="#f45342" if priority == "high" else "#4CAF50"
                )
            )
        )

        # Send
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
        return response

    except Exception as e:
        print(f"FCM Send Error: {e}")
        # In production, we would handle invalid tokens (cleanup DB) here.
        return None


def send_disaster_alert(token: str, disaster_type: str, message: str):
    """
    CHANNEL A: MANDATORY WARNINGS
    Sends a High-Priority alert with sound/vibration.
    """
    title = f"⚠️ CRITICAL: {disaster_type} Alert"
    send_push_notification(
        token=token,
        title=title,
        body=message,
        data={"type": "disaster", "category": disaster_type},
        priority="high"
    )

def send_good_news(token: str, category: str, message: str):
    """
    CHANNEL B: GOOD INFO
    Sends a Normal-Priority update (e.g., Weekly Weather, Stargazing).
    """
    emojis = {
        "weather": "☀️",
        "astronomy": "✨",
        "general": "🌍"
    }
    icon = emojis.get(category, "📢")
    title = f"{icon} EARTH: {category.capitalize()} Update"
    
    send_push_notification(
        token=token,
        title=title,
        body=message,
        data={"type": "info", "category": category},
        priority="normal"
    )