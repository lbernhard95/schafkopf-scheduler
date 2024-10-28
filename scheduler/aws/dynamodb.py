import json
from datetime import datetime
from typing import List, Literal, Optional

import boto3
from pydantic import BaseModel, Field


class EmailItem(BaseModel):
    email: str


class EmailTable:
    def __init__(self):
        self._table = boto3.resource("dynamodb").Table("schafkopf_emails")

    def add(self, email: EmailItem):
        self._table.put_item(Item=json.loads(email.model_dump_json()))

    def load_all(self) -> List[EmailItem]:
        try:
            response = self._table.scan()
            items = response["Items"]
            while "LastEvaluatedKey" in response:
                response = self._table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
                items.extend(response["Items"])
            result = []
            for item in items:
                try:
                    result.append(EmailItem(**item))
                except Exception as e:
                    print(f"Could not load {item}: {e}")
            return result
        except Exception as e:
            raise RuntimeError(
                f"Could not load emails: {e}"
            )



class PollItem(BaseModel):
    running_poll_id: Optional[str] = None
    start_next_poll_date: Optional[datetime] = None


class PollTable:
    POLL_ITEM_UUID = '021dae01-ac37-4c3c-bc6c-952d3e4a57d5'
    def __init__(self):
        self._table = boto3.resource("dynamodb").Table("schafkopf_polls")

    def load(self) -> PollItem:
        try:
            response = self._table.query(
                KeyConditionExpression=f"uuid = :a",
                ExpressionAttributeValues={":a": self.POLL_ITEM_UUID},
                Limit=1,
            )
            return PollItem(**response["Items"][0])
        except Exception:
            raise ValueError(
                f"Could not find poll item"
            )

    def update(self, poll_item: PollItem):
        item_dict = json.loads(poll_item.model_dump_json())
        item_dict['uuid'] = self.POLL_ITEM_UUID
        self._table.put_item(Item=item_dict)