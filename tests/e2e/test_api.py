from datetime import datetime
from unittest.mock import ANY

from moto import mock_aws
from freezegun import freeze_time
from fastapi.testclient import TestClient

from schafkopf.api.api import app
from tests.e2e import mock_dynamodb
from schafkopf.core.dynamodb.poll_table import POLL_ITEM_UUID


@freeze_time("2023-01-01T18:30:00")
@mock_aws
def test_subscribe_to_new_schafkopf_rounds_(mock_gmail_send):
    mail_table = mock_dynamodb.create_emails_table()
    poll_table = mock_dynamodb.create_polls_table()
    poll_table.add(
        {
            "uuid": POLL_ITEM_UUID,
            "running_poll_id": "123",
            "start_next_poll_date": datetime(2023, 1, 15, 18, 30),
            "new_poll_email_sent": datetime(2023, 1, 1, 10, 0),
        }
    )

    rsp = TestClient(app).post("/subscribe", json={"email": "NEW-test@email.com"})

    mails = mail_table.scan()

    assert rsp.status_code == 200
    assert rsp.json() == {"email": "new-test@email.com"}
    assert {"email": "new-test@email.com"} in mails
    assert len(mails) == 3
    mock_gmail_send.assert_called_with(receivers=ANY, subject="Welcome to our Schafkopf Round", body=ANY)


@mock_aws
def test_delete_from_mail_list(mock_gmail_send):
    mail_table = mock_dynamodb.create_emails_table()
    mail_table.add({"email": "delete@mail.com"})

    rsp = TestClient(app).delete("/subscriber", params={"email": "DeLete@mail.com"})

    mails = mail_table.scan()
    assert rsp.status_code == 200
    assert rsp.json() == {"email": "delete@mail.com"}
    assert {"email": "delete@mail.com"} not in mails
    assert len(mails) == 2


@mock_aws
def test_get_subscriber_count(mock_gmail_send):
    mail_table = mock_dynamodb.create_emails_table()

    rsp = TestClient(app).get("/subscribers/count")

    mails = mail_table.scan()
    assert rsp.status_code == 200
    assert rsp.json()["count"] == len(mails)
    assert len(mails) == 2


@mock_aws
def test_get_poll():
    poll_table = mock_dynamodb.create_polls_table()
    poll_table.add(
        {
            "uuid": POLL_ITEM_UUID,
            "running_poll_id": "123",
            "start_next_poll_date": datetime(2023, 1, 1, 18, 31),
            "new_poll_email_sent": datetime(2023, 1, 1, 10, 0),
        }
    )

    rsp = TestClient(app).get("/poll")

    assert rsp.status_code == 200
    assert rsp.json() == {
        "bitpoll_link": "https://bitpoll.de/poll/123",
        "start_next_poll_date": "2023-01-01T18:31:00",
        "next_schafkopf_event": None,
        "current_poll_started": "2023-01-01T10:00:00",
    }
