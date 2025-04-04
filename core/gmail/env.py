from pydantic import Field

from core.env import BaseEnvironment


class GmailEnv(BaseEnvironment):
    gmail_username: str = Field(default="not-set", alias="GMAIL_SENDER_ADDRESS")
    gmail_password: str = Field(default="not-set", alias="GMAIL_SENDER_PASSWORD")
