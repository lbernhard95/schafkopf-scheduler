from scheduler import gmail, bitpoll, scheduler


def start_new_poll():
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
        receivers=gmail.load_receivers(),
        bitpoll_link=new_poll_website
    )
    # todo store poll_id
    print("Done")


def get_best_date_for_poll():
    poll_id = ""
    page = bitpoll.get_poll_webpage(poll_id=poll_id)
    votes = bitpoll.collect_vote_dates(page)
    best_date = scheduler.find_best_date(votes)
    print("Most promising date:", best_date)

    if best_date:
        print("Found valid date, sending out invitation")
        gmail.send_schafkopf_meeting_invitation(
            receivers=gmail.load_receivers(),
            day=best_date,
            bitpoll_link=bitpoll.get_website_from_poll_id(poll_id)
        )
    # todo delete poll id from db?
    # calculate when next scheduling should happen?
    print("Done")


if __name__ == '__main__':
    start_new_poll()