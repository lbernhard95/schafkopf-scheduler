import requests

from core.gmail.client import GmailClient


URL = "https://ebg-muenchen-west.de/wohnungsangebote/"


def lambda_handler():
    if load_available_apartments():
        print("Apartments available")
        notify_on_available_apartments()
    else:
        print("No apartments available")


def load_available_apartments() -> bool:
    rsp = requests.get("https://ebg-muenchen-west.de/wohnungsangebote/")
    if "keine freien Wohnungen verfügbar" in rsp.text:
        return False
    return True


def notify_on_available_apartments():
    GmailClient().send(
        receivers=["L.J.Bernhard@web.de"],
        subject="Apartments available at EBG München West",
        body="Apartments are available! Check https://ebg-muenchen-west.de/wohnungsangebote/",
    )


if __name__ == "__main__":
    lambda_handler()
