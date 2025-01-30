import boto3

from schafkopf.boto3.dynamodb import DynamoDBTable


def create_emails_table(emails: list[str] = None) -> DynamoDBTable:
    tabel_name = "schafkopf_emails"
    dynamo_db = boto3.resource("dynamodb", region_name="eu-central-1")
    boto_table = dynamo_db.create_table(
        TableName=tabel_name,
        KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    boto_table.meta.client.get_waiter("table_exists").wait(TableName=tabel_name)
    table = DynamoDBTable(tabel_name)
    table.add_many(
        [{"email": m} for m in emails or ["test@example.com", "test2@example.com"]]
    )
    return table


def create_polls_table() -> DynamoDBTable:
    tabel_name = "schafkopf_polls"
    dynamo_db = boto3.resource("dynamodb", region_name="eu-central-1")
    boto_table = dynamo_db.create_table(
        TableName=tabel_name,
        KeySchema=[{"AttributeName": "uuid", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "uuid", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    boto_table.meta.client.get_waiter("table_exists").wait(TableName=tabel_name)
    return DynamoDBTable(tabel_name)
