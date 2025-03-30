from pydantic import Field

from core.env import BaseEnvironment


class GmailEnv(BaseEnvironment):
    gmail_username: str = Field(alias="GMAIL_SENDER_ADDRESS")
    gmail_password: str = Field(alias="GMAIL_SENDER_PASSWORD")
