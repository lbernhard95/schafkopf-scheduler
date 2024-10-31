import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

POLL_ITEM_UUID = '021dae01-ac37-4c3c-bc6c-952d3e4a57d5'


class PollItem(BaseModel):
    running_poll_id: str
    start_next_poll_date: datetime
    new_poll_email_sent: datetime
    event_invitation_email_sent: Optional[datetime] = None
    next_schafkopf_event: Optional[datetime] = None

    @staticmethod
    def create_new(poll_id: str, next_poll_date: datetime) -> "PollItem":
        return PollItem(
            running_poll_id=poll_id,
            start_next_poll_date=next_poll_date,
            new_poll_email_sent=datetime.now(),
            next_schafkopf_event=None
        )

    def event_scheduled_update(self, event_date: datetime):
        self.start_next_poll_date = event_date
        self.next_schafkopf_event = event_date
        self.event_invitation_email_sent = datetime.now()

    def poll_is_running(self) -> bool:
        return (
            self.running_poll_id and
            datetime.now() < self.start_next_poll_date and
            self.event_invitation_email_sent is None
        )

    def is_time_to_start_new_poll(self) -> bool:
        return datetime.now() >= self.start_next_poll_date


def load(dynamodb) -> PollItem:
    try:
        table = dynamodb.Table("schafkopf_polls")
        response = table.query(
            KeyConditionExpression=f"#u = :a",
            ExpressionAttributeNames={'#u': "uuid"},
            ExpressionAttributeValues={":a": POLL_ITEM_UUID},
            Limit=1,
        )
        return PollItem(**response["Items"][0])
    except Exception as e:
        raise ValueError(
            f"Could not find poll item", e
        )

def update(dynamodb, poll_item: PollItem):
    table = dynamodb.Table("schafkopf_polls")
    item_dict = json.loads(poll_item.model_dump_json())
    item_dict['uuid'] = POLL_ITEM_UUID
    table.put_item(Item=item_dict)