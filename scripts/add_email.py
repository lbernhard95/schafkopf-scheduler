import boto3

from scheduler import env
from scheduler.dynamodb import poll_table, email_table
from scheduler.dynamodb.email_table import EmailItem
from scheduler.dynamodb.poll_table import PollItem

dynamodb = boto3.resource("dynamodb")
poll_table.update(dynamodb, PollItem())

email_table.add(dynamodb, EmailItem(email="lukas.j.bernhard@gmail.com"))