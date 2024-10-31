import json
from typing import List

from pydantic import BaseModel

from schafkopf.core import env


class EmailItem(BaseModel):
    email: str


def add(dynamodb, email: EmailItem):
    table = dynamodb.Table("schafkopf_emails")
    table.put_item(Item=json.loads(email.model_dump_json()))


def load_all_mails(dynamodb) -> List[str]:
    registered = [i.email for i in load_all(dynamodb)]
    return list(set(registered + [env.get_gmail_sender_address()]))

def count(dynamodb) -> int:
    table = dynamodb.Table("schafkopf_emails")
    item_count = table.item_count
    return item_count

def load_all(dynamodb) -> List[EmailItem]:
    try:
        table = dynamodb.Table("schafkopf_emails")
        response = table.scan()
        items = response["Items"]
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
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
