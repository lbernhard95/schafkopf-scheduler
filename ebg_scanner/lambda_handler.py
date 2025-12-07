import requests

from core.gmail.client import GmailClient


URL = "https://ebg-muenchen-west.de/wohnungsangebote/"


def lambda_handler(event, context):
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
        body="""
        <html>
          <body>
            <p>
              Apartments are available!<br>
              Check the latest offers here:<br>
              <a href="https://ebg-muenchen-west.de/wohnungsangebote/" target="_blank">
                EBG München West Apartment Listings
              </a>
            </p>
          </body>
        </html>
        """,
    )


if __name__ == "__main__":
    notify_on_available_apartments()
