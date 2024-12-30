from unittest.mock import ANY
from freezegun import freeze_time
from datetime import datetime
import responses

from moto import mock_aws
from schafkopf.core.dynamodb.poll_table import POLL_ITEM_UUID
from schafkopf.scheduler.lambda_handler import lambda_handler
from tests.e2e import mock_dynamodb, mock_bitpoll


@freeze_time("2023-01-01T18:30:00")
@mock_aws
def test_create_new_poll(mock_gmail_send):
    mock_dynamodb.create_emails_table()
    poll_table = mock_dynamodb.create_polls_table()
    poll_table.add({
        "uuid": POLL_ITEM_UUID,
        "running_poll_id": "123",
        "start_next_poll_date": datetime(2023, 1, 1, 18, 31),
        "new_poll_email_sent": datetime(2023, 1, 1, 10, 0),
    })

    with responses.RequestsMock(
            assert_all_requests_are_fired=False
    ) as rsps:
        mock_bitpoll.create_new_poll_endpionts(rsps)
        lambda_handler({}, None)

    poll_item = poll_table.scan()[0]
    assert poll_item["running_poll_id"] == mock_bitpoll.NEW_POLL_ID
    assert poll_item["start_next_poll_date"] == "2023-01-13T18:30:00"
    assert poll_item["new_poll_email_sent"] == "2023-01-01T18:30:00"
    assert poll_item["next_schafkopf_event"] is None
    assert poll_item["uuid"] == POLL_ITEM_UUID


    mock_gmail_send.assert_called_with(
        receivers=ANY,
        subject="New Schafkopf Round",
        body=ANY
    )
    mock_receivers = mock_gmail_send.call_args[1]['receivers']
    assert set(mock_receivers) == {'test2@example.com', 'test@example.com'}
