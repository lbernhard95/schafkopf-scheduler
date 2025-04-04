from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import List

from core import log
from core.gmail.client import GmailClient


def send_beachbooker_run_logs(receivers: List[str]):
    GmailClient().send(
        subject="Beachbooker ran",
        body="Have a look at the logs to find out what happened",
        receivers=receivers,
        attachment=create_log_attachement(log.log_file),
    )


def create_log_attachement(log_file_path: Path) -> MIMEBase:
    with open(log_file_path, "r") as f:
        log_content = f.read()
    # Attach the iCalendar file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(log_content.encode("utf-8"))
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename=beachbooker_log_{datetime.now()}.ics")
    return part
