from datetime import datetime, timedelta, date
from typing import Optional, List

from pydantic import BaseModel, computed_field

from schafkopf.boto3.dynamodb import DynamoDBTable

PARTITION_KEY_NAME = "poll"
SORT_KEY_NAME = "sort_key"

class Poll(BaseModel):
    url: str
    poll_created: datetime
    upcoming_event: Optional[datetime] = None
    next_poll_day: Optional[date] = None
    attendees: Optional[List[str]] = None

    @computed_field
    def partition_key(self) -> str:
        return PARTITION_KEY_NAME

    @computed_field
    def sort_key(self) -> str:
        return str(self.poll_created)

    @staticmethod
    def create_new(url: str) -> "Poll":
        now = datetime.now()
        return Poll(
            url=url,
            poll_created=now,
            upcoming_event=None,
            next_poll_day=(now + timedelta(days=14)).date(),
        )

    def set_upcoming_event(self, event_date: datetime, attendees: List[str]):
        self.upcoming_event = event_date
        self.next_poll_day = (event_date + timedelta(days=2)).date()
        self.attendees = attendees

    def poll_is_running(self) -> bool:
        return (
            not self.is_time_to_start_new_poll() and
            self.upcoming_event is None
        )

    def is_time_to_start_new_poll(self) -> bool:
        return date.today() >= self.next_poll_day


class PollTable(DynamoDBTable):
    def __init__(self):
        super().__init__("schafkopf_scheduler")

    def get_current_poll(self) -> Poll:
        response = self.query(
            key_condition="partition_key = :a",
            expression_values={":a": PARTITION_KEY_NAME},
            scan_index="backwards",
            limit=1,
        )
        return Poll(**response[0])
