import responses

NEW_POLL_ID = "new-poll-id"
TEST_CSRF_TOKEN = "test-csrf-token"


def create_new_poll_endpoints(rsps: responses.RequestsMock):
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


def create_event_found_endpoints(rsps: responses.RequestsMock, poll_id: str):
    rsps.add(
        responses.GET,
        f"https://bitpoll.de/poll/{poll_id}",
        body=f"""
        <html>
            <table id="poll">
                <thead><tr>
                    <th colspan="1" rowspan="1" class="choice-group">
                        Tue, 9. Jan. 2023
                    </th>
                    <th colspan="1" rowspan="1" class="choice-group">
                        Wed, 10. Jan. 2023
                    </th>
                    <th colspan="1" rowspan="1" class="choice-group">
                        Thu, 11. Jan. 2023
                    </th>
                </tr></thead>
                <tfoot>
                    <tr class="print-only">
                        <th>
                            Score
                        </th>
                    </tr>
                    <tr class="print-only">
                        <th>Details</th>
                        <td>
                            <div class="value">1<span class="fa fa-ban"></span></div>
                            <div class="value">2<span class="fa fa-check"></span></div>
                            <div class="value">2<span class="fa fa-question"></span></div>
                        </td>
                        <td>
                            <div class="value">2<span class="fa fa-ban"></span></div>
                            <div class="value">5<span class="fa fa-check"></span></div>
                            <div class="value">1<span class="fa fa-question"></span></div>
                        </td>
                        <td>
                            <div class="value">1<span class="fa fa-ban"></span></div>
                            <div class="value">3<span class="fa fa-check"></span></div>
                            <div class="value">4<span class="fa fa-question"></span></div>
                        </td>
                    </tr>
                </tfoot>
            </table>
        </html>"""
    )