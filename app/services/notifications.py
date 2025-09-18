import time

def send_welcome_email(email: str) -> None:
    """
    ✉️ Simulation d'envoi de notification/email de bienvenue.
    En prod : brancher un SMTP, un provider (Sendgrid, Mailgun) ou un message queue.
    """
    # Simuler une latence réseau (facultatif, visible en logs)
    time.sleep(0.2)
    print(f"[NOTIFY] Bienvenue {email} ! (notification envoyée)")
