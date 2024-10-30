import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

POLL_ITEM_UUID = '021dae01-ac37-4c3c-bc6c-952d3e4a57d5'


class PollItem(BaseModel):
    running_poll_id: Optional[str] = None
    start_next_poll_date: Optional[datetime] = None

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