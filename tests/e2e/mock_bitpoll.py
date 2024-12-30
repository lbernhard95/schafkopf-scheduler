import pytest
import responses

NEW_POLL_ID = "new-poll-id"
TEST_CSRF_TOKEN = "test-csrf-token"


def create_new_poll_endpionts(rsps: responses.RequestsMock):
    rsps.add(
        responses.GET,
        "https://bitpoll.de/",
        body=f"""
        <html>
            <input type="hidden" name="csrfmiddlewaretoken" value="{TEST_CSRF_TOKEN}">
        </html>"""
    )
    rsps.add(
        responses.POST,
        "https://bitpoll.de/",
        body=f"""
        <html>
            <a data-shortcut="g c" href="/poll/{NEW_POLL_ID}/edit/choices/"></a>
        </html>"""
    )
    rsps.add(
        responses.POST,
        f"https://bitpoll.de/poll/{NEW_POLL_ID}/edit/choices/date/",
        body="ok"
    )