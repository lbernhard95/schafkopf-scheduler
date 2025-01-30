import json

import boto3

from typing import List, Dict, Optional, Literal, Union

from pydantic import BaseModel

from schafkopf.core import env


class DynamoDBTable:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.table = boto3.resource("dynamodb").Table(table_name)

    def add(self, item: Union[Dict, BaseModel]):
        if env.read_only():
            print(f"Read only, not adding: {item}")
            return
        if isinstance(item, BaseModel):
            item = item.model_dump()
        self.table.put_item(Item=json.loads(json.dumps(item, default=str)))

    def update(self, item: Union[Dict, BaseModel]):
        if env.read_only():
            print(f"Read only, not updating: {item}")
            return
        self.add(item)

    def add_many(self, items: List[Union[Dict, BaseModel]]):
        if env.read_only():
            print(f"Read only, not adding: {items}")
            return
        with self.table.batch_writer() as batch:
            for item in items:
                if isinstance(item, BaseModel):
                    item = item.model_dump()
                batch.put_item(Item=item)

    def delete(self, key: Dict):
        if env.read_only():
            print(f"Read only, not deleting: {key}")
            return
        self.table.delete_item(Key=key)

    def count(self) -> int:
        return self.table.item_count

    def query(
        self, key_condition: str,
        expression_values: Optional[Dict] = None,
        scan_index: Literal["forwards", "backwards"] = "forwards",
        limit: int = 1,
    ) -> List[Dict]:
        response = self.table.query(
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=expression_values if expression_values else {},
            ScanIndexForward=scan_index == "forwards",
            Limit=limit,
        )
        return response["Items"]

    def scan(self) -> List[Dict]:
        try:
            response = self.table.scan()
            items = response["Items"]
            while "LastEvaluatedKey" in response:
                response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
                items.extend(response["Items"])
            result = []
            for item in items:
                try:
                    result.append(item)
                except Exception as e:
                    print(f"Could not load {item}: {e}")
            return result
        except Exception as e:
            raise RuntimeError(
                f"Could not load items from {self.table_name}: {e}"
            )
