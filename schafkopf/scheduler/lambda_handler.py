from typing import List

import boto3

from schafkopf.scheduler import scheduler
from schafkopf.core import gmail, bitpoll
from schafkopf.core.dynamodb import email_table
from schafkopf.core.dynamodb import poll_table
from schafkopf.core.dynamodb.poll_table import PollItem


def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource("dynamodb")
    poll = poll_table.load(dynamodb)
    subscribed_emails = email_table.load_all_mails(dynamodb)
    if poll.poll_is_running():
        new_poll = schedule_next_schafkopf_event(subscribed_emails, poll)
    elif poll.is_time_to_start_new_poll():
        new_poll = start_new_poll(subscribed_emails)
    else:
        print("No action required, waiting before scheduling new poll:", poll)
        return
    print("Store new poll item:", new_poll)
    poll_table.update(dynamodb, new_poll)


def start_new_poll(subscribed_emails) -> PollItem:
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
        receivers=subscribed_emails,
        bitpoll_link=new_poll_website
    )
    return PollItem.create_new(
        poll_id=poll_id,
        next_poll_date=max(dates),
    )

def schedule_next_schafkopf_event(emails: List[str], poll: PollItem) -> PollItem:
    poll_website = bitpoll.get_website_from_poll_id(poll.running_poll_id)
    print("Try to schedule next schafkopf event for:", poll_website)
    voting_table = bitpoll.get_voting_table(poll_id=poll.running_poll_id)
    votes = bitpoll.collect_vote_dates(voting_table)
    best_vote = scheduler.find_best_date(votes)
    print("Most promising vote:", best_vote)

    if best_vote:
        print("Found valid date, sending out invitation")
        best_date = best_vote.date
        gmail.send_schafkopf_meeting_invitation(
            receivers=emails,
            start=best_date,
            bitpoll_link=poll_website
        )
        poll.event_scheduled_update(event_date=best_date)
    return poll


if __name__ == '__main__':
    lambda_handler({}, {})