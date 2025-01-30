from pydantic import BaseModel, computed_field, constr

from schafkopf.boto3.dynamodb import DynamoDBTable


class Subscriber(BaseModel):
    email: constr(to_lower=True)

    @computed_field
    def partition_key(self) -> str:
        return self.email


class SubscriberTable(DynamoDBTable):
    def __init__(self):
        super().__init__("schafkopf_scheduler")

    def delete(self, email: str):
        super().delete({"partition_key": email.lower()})

    def get_all_mails(self) -> list[str]:
        return [
            Subscriber(**item).email
            for item in self.scan()
        ]