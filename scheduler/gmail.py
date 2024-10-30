import locale
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Optional

from scheduler import env


def send_bitpoll_invitation(receivers: List[str], bitpoll_link: str):
    html = load_html_template(f"{env.BASE_PATH}/templates/poll_invitation.html")
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)

    send(
        receivers=receivers,
        subject="New Schafkopf Round",
        body=MIMEText(html, "html")
    )


def send_schafkopf_meeting_invitation(receivers: List[str], start: datetime, bitpoll_link: str):
    html = load_html_template(f"{env.BASE_PATH}/templates/schafkopf_scheduled.html")
    html = html.replace("SCHEDULED_DATE_PLACEHOLDER", format_datetime(start))
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)

    send(
        receivers=receivers,
        subject=f"Schafkopfen on {start.strftime('%d.%m')}",
        body=MIMEText(html, "html"),
        attachment=create_calendar_entry(
            summary="[at] Schafkopfen",
            start=start, end=start.replace(hour=23, minute=0),
        )
    )


def send(
    receivers: List[str],
    subject: str,
    body: MIMEText,
    attachment: Optional[MIMEBase]=None
):
    sender = env.get_gmail_sender_address()
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ", ".join(receivers)
    message['Subject'] = subject
    message.attach(body)
    if attachment:
        message.attach(attachment)

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(sender, env.get_gmail_sender_pw())
    smtpserver.sendmail(sender, receivers, message.as_string())
    smtpserver.close()


def create_calendar_entry(start: datetime, end: datetime, summary: str) -> MIMEBase:
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Schafkopf Scheduler//[at] Schafkopf
BEGIN:VEVENT
UID:{env.get_gmail_sender_address()}
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}
DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}
SUMMARY:[at] Schafkopfen
DESCRIPTION:{summary}
END:VEVENT
END:VCALENDAR
"""

    # Attach the iCalendar file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(ics_content.encode("utf-8"))
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename=schafkopfen.ics"
    )
    return part


def format_datetime(dt: datetime):
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8') 
    weekday_name = dt.strftime('%A')
    month_name = dt.strftime('%B')
    day = dt.day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    formatted_day = f"{day}{suffix}"
    formatted_time = dt.strftime('%H:%M')
    return f"{weekday_name}, {month_name} {formatted_day} at {formatted_time}"


def load_html_template(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as f:
        return f.read()