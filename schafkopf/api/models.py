from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schafkopf.boto3.email import Subscriber
from schafkopf.boto3.poll import Poll

class SubscribeRequest(BaseModel):
    email: str

    def to_subscriber(self) -> Subscriber:
        return Subscriber(email=self.email)


class SubscribeResponse(BaseModel):
    email: str


class SubscribeCountResponse(BaseModel):
    count: int

class PollResponse(BaseModel):
    bitpoll_link: str
    start_next_poll_date: datetime
    next_schafkopf_event: Optional[datetime] = None
    current_poll_started: datetime


    @staticmethod
    def from_item(item: Poll) -> "PollResponse":
        return PollResponse(
            bitpoll_link=item.url,
            next_schafkopf_event=item.upcoming_event,
            start_next_poll_date=datetime.combine(item.next_poll_day, datetime.min.time()),
            current_poll_started=item.poll_created
        )