from datetime import datetime, timedelta

from beachbooker import gmail, config
from beachbooker.env import Environment
from core.log import logger
from functions import get_driver, close_driver, login, find_and_book_slots


def main():
    driver = get_driver()
    env = Environment.load()
    login(driver, username=env.zhs_username, password=env.zhs_password)

    dt = datetime.now() + timedelta(days=7)  # Normally +8, but with time zone issues on AWS +9
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
            logger.info("Booking successful!")
            break
        elif res == "captcha":
            logger.info(f"Google captcha not passed. This was attempt {captcha_count + 1}/{captcha_max}")
            captcha_count += 1
            if captcha_count >= captcha_max:
                logger.info("I have had enough!")
                captcha_count = 0
                i += 1
            else:
                logger.info("Trying again.")
        elif res == "error":
            logger.error("Error!")
            i += 1
            captcha_count = 0
        elif res == "mindestbuchungszeit":
            logger.info("Mindestbuchungszeit bug")
            i += 1
            captcha_count = 0
        elif res == "not_enough_slots":
            logger.info("Not enough slots available.")
            i += 1
            captcha_count = 0

    close_driver(driver)
    logger.info("Sending Logs via mail")
    gmail.send_beachbooker_run_logs(receivers=config.NOTIFICATION_RECEIVER_EMAILS)


if __name__ == "__main__":
    main()
