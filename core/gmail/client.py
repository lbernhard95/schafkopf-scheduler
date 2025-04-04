import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from typing import List, Optional

from core.gmail.env import GmailEnv


class GmailClient:
    def __init__(self):
        self._env = GmailEnv.load()

    def send(
        self,
        receivers: List[str],
        subject: str,
        body: str,
        attachment: Optional[MIMEBase] = None,
    ):
        if self._env.read_only:
            print(f"Read only, not sending email '{subject}' to {receivers}")
            return

        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpserver.ehlo()
        smtpserver.login(self._env.gmail_username, self._env.gmail_password)
        for receiver in receivers:
            message = MIMEMultipart()
            message["From"] = self._env.gmail_username
            message["To"] = receiver
            message["Subject"] = subject
            message.attach(MIMEText(body.replace("RECEIVER_EMAIL", receiver), "html"))
            if attachment:
                message.attach(attachment)
            msg = message.as_string()
            smtpserver.sendmail(self._env.gmail_username, receiver, msg)
        smtpserver.close()
