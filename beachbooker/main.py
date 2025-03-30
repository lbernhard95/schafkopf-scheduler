from datetime import datetime, timedelta

from beachbooker import config
from beachbooker.env import Environment
from core.gmail.client import GmailClient
from functions import get_driver, close_driver, login, find_and_book_slots


def main():
    gmail = GmailClient()
    gmail.send(
        subject="Beachbooker started",
        body="Beachbooker has started",
        receivers=config.NOTIFICATION_RECEIVER_EMAILS,
    )
    driver = get_driver()
    env = Environment.load()
    login(driver, username=env.zhs_username, password=env.zhs_password)

    dt = datetime.now() + timedelta(
        days=7
    )  # Normally +8, but with time zone issues on AWS +9
    # dt = datetime.now() + timedelta(days=8)
    booking_date = dt.strftime("%Y-%m-%d")

    # Note: Sets with a smaller index are prioritized higher!
    booking_times_sets = [["13:30"], ["14:30"]]

    i = 0
    captcha_count = 0
    captcha_max = 10

    while i < len(booking_times_sets):

        booking_times = booking_times_sets[i]
        res = find_and_book_slots(driver, booking_date, booking_times)

        if res == "success":
            print("Booking successful!")
            break
        elif res == "captcha":
            print(
                f"Google captcha not passed. This was attempt {captcha_count+1}/{captcha_max}"
            )
            captcha_count += 1
            if captcha_count >= captcha_max:
                print("I have had enough!")
                captcha_count = 0
                i += 1
            else:
                print("Trying again.")
        elif res == "error":
            print("Error!")
            i += 1
            captcha_count = 0
        elif res == "mindestbuchungszeit":
            print("Mindestbuchungszeit bug")
            i += 1
            captcha_count = 0
        elif res == "not_enough_slots":
            print("Not enough slots available.")
            i += 1
            captcha_count = 0

    close_driver(driver)


if __name__ == "__main__":
    main()
