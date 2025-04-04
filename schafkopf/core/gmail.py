from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List

from core.gmail import utils
from core.gmail.client import GmailClient
from schafkopf.core import env


def send_bitpoll_invitation(receivers: List[str], bitpoll_link: str):
    html = utils.load_html_template(f"{env.BASE_PATH}/schafkopf/templates/poll_invitation.html")
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)

    GmailClient().send(receivers=receivers, subject="New Schafkopf Round", body=html)


def send_welcome_with_running_bitpoll(receiver: str, bitpoll_link: str):
    html = utils.load_html_template(f"{env.BASE_PATH}/schafkopf/templates/welcome_with_poll_running.html")
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)

    GmailClient().send(receivers=[receiver], subject="Welcome to our Schafkopf Round", body=html)


def send_schafkopf_meeting_invitation(receivers: List[str], attendees: List[str], start: datetime, bitpoll_link: str):
    html = utils.load_html_template(f"{env.BASE_PATH}/schafkopf/templates/schafkopf_scheduled.html")
    html = html.replace("SCHEDULED_DATE_PLACEHOLDER", format_datetime(start))
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)
    html = html.replace("ATTENDEE_LIST_PLACEHOLDER", "\n".join(f"<li>{a}</li>" for a in attendees))

    GmailClient().send(
        receivers=receivers,
        subject=f"Schafkopfen on {start.strftime('%d.%m')}",
        body=html,
        attachment=create_calendar_entry(
            summary="[at] Schafkopfen",
            start=start,
        ),
    )


def send_welcome_with_meeting_invitation(receiver: str, start: datetime, bitpoll_link: str):
    html = utils.load_html_template(f"{env.BASE_PATH}/schafkopf/templates/welcome_with_event_scheduled.html")
    html = html.replace("SCHEDULED_DATE_PLACEHOLDER", format_datetime(start))
    html = html.replace("YOUR_BITPOLL_LINK_HERE", bitpoll_link)

    GmailClient().send(
        receivers=[receiver],
        subject="Welcome to our Schafkopf Round",
        body=html,
        attachment=create_calendar_entry(summary="[at] Schafkopfen", start=start),
    )


def create_calendar_entry(start: datetime, summary: str) -> MIMEBase:
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Schafkopf Scheduler//[at] Schafkopf
BEGIN:VEVENT
UID:{env.get_gmail_sender_address()}
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%S')}
DTSTART:{start.strftime('%Y%m%dT%H%M%S')}
DTEND:{start.replace(hour=23, minute=0).strftime('%Y%m%dT%H%M%S')}
SUMMARY:[at] Schafkopfen
DESCRIPTION:{summary}
END:VEVENT
END:VCALENDAR
"""

    # Attach the iCalendar file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(ics_content.encode("utf-8"))
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=schafkopfen.ics")
    return part


def format_datetime(dt: datetime):
    weekday_name = dt.strftime("%A")
    month_name = dt.strftime("%B")
    day = dt.day
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    formatted_day = f"{day}{suffix}"
    formatted_time = dt.strftime("%H:%M")
    return f"{weekday_name}, {month_name} {formatted_day} at {formatted_time}"
