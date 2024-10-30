from datetime import datetime

import boto3

from scheduler import gmail, bitpoll, scheduler
from scheduler.dynamodb import poll_table, email_table
from scheduler.dynamodb.poll_table import PollItem


def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource("dynamodb")
    poll_item = poll_table.load(dynamodb)
    if is_poll_running(poll_item):
        schedule_next_schafkopf_event(dynamodb, poll_item.running_poll_id)
        return

    new_poll_item = start_new_poll(dynamodb)
    print("Store new poll item:", new_poll_item)
    poll_table.update(dynamodb, new_poll_item)


def is_poll_running(item: PollItem) -> bool:
    return item.running_poll_id and datetime.now() < item.start_next_poll_date


def start_new_poll(dynamodb) -> PollItem:
    print("Start a new poll")
    print("Generate csrf token")
    csrf_token = bitpoll.get_valid_csrf_token()
    print("csrf token:", csrf_token)

    print("Create new poll")
    poll_id = bitpoll.create_new_poll(csrf_token=csrf_token)
    print("New poll created")

    print("Generate dates to vote on")
    dates = scheduler.generate_working_days_for_next_weeks(weeks=2)

    print("Add dates to poll as choices")
    bitpoll.add_choices_to_poll(poll_id=poll_id, csrf_token=csrf_token, dates=dates)
    new_poll_website = bitpoll.get_website_from_poll_id(poll_id)
    print("Poll created:", new_poll_website)

    print("Send out email notifications")
    gmail.send_bitpoll_invitation(
        receivers=email_table.load_all_mails(dynamodb),
        bitpoll_link=new_poll_website
    )
    return PollItem(
        running_poll_id=poll_id,
        start_next_poll_date=max(dates)
    )


def schedule_next_schafkopf_event(dynamodb, poll_id: str):
    poll_website = bitpoll.get_website_from_poll_id(poll_id)
    print("Try to schedule next schafkopf event for:", poll_website)
    page = bitpoll.get_poll_webpage(poll_id=poll_id)
    votes = bitpoll.collect_vote_dates(page)
    best_date = scheduler.find_best_date(votes)
    print("Most promising date:", best_date)

    if best_date:
        print("Found valid date, sending out invitation")
        gmail.send_schafkopf_meeting_invitation(
            receivers=email_table.load_all_mails(dynamodb),
            day=best_date.date,
            bitpoll_link=poll_website
        )


if __name__ == '__main__':
    from scheduler import env  # ensure loading aws credentials
    lambda_handler({}, {})