"""Email notifier via SMTP. Credentials come from the environment / config."""
from __future__ import annotations

import smtplib
from email.message import EmailMessage

from .base import Notifier


class EmailNotifier(Notifier):
    def __init__(self, email_cfg: dict):
        self.to = email_cfg["to"]
        self.sender = email_cfg.get("sender") or email_cfg["to"]
        self.host = email_cfg["smtp_host"]
        self.port = int(email_cfg.get("smtp_port", 587))
        self.user = email_cfg.get("smtp_user") or ""
        self.password = email_cfg.get("smtp_password") or ""

    def notify(self, *, subject: str, message: str, link: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.to
        msg.set_content(f"{message}\n\nReview the draft here:\n{link}\n")

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            if self.user:
                server.login(self.user, self.password)
            server.send_message(msg)
