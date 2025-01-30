from dotenv import load_dotenv
import os
import pathlib


BASE_PATH = pathlib.Path(__file__).parent.parent.parent.resolve()

load_dotenv()


def read_only() -> bool:
    return os.getenv("READ_ONLY") == "true"


def get_gmail_sender_address() -> str:
    return os.getenv("GMAIL_SENDER_ADDRESS")


def get_gmail_sender_pw() -> str:
    return os.getenv("GMAIL_SENDER_PASSWORD")
