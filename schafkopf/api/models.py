from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core import bitpoll
from core.dynamodb.email_table import EmailItem
from core.dynamodb.poll_table import PollItem


class SubscribeRequest(BaseModel):
    email: str

    def to_email_item(self) -> EmailItem:
        return EmailItem(email=self.email)


class SubscribeResponse(BaseModel):
    email: str


class PollResponse(BaseModel):
    bitpoll_link: str
    start_next_poll_date: datetime
    next_schafkopf_event: datetime
    current_poll_started: datetime

    @staticmethod
    def from_item(item: PollItem) -> "PollResponse":
        return PollResponse(
            bitpoll_link=bitpoll.get_website_from_poll_id(item.running_poll_id),
            next_schafkopf_event=item.next_schafkopf_event,
            start_next_poll_date=item.start_next_poll_date,
            current_poll_started=item.new_poll_email_sent
        )