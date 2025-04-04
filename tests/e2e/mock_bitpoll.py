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
        </html>""",
    )
    rsps.add(
        responses.POST,
        "https://bitpoll.de/",
        body=f"""
        <html>
            <a data-shortcut="g c" href="/poll/{NEW_POLL_ID}/edit/choices/"></a>
        </html>""",
    )
    rsps.add(
        responses.POST,
        f"https://bitpoll.de/poll/{NEW_POLL_ID}/edit/choices/date/",
        body="ok",
    )


def create_event_found_endpoints(rsps: responses.RequestsMock, poll_id: str):
    rsps.add(
        responses.GET,
        f"https://bitpoll.de/poll/{poll_id}",
        body="""
        <table class="table poll auto-width" id="poll">
   <tbody>
      <tr class="vote ">
         <td class="author" data-toggle="popover" data-trigger="hover" data-container="body" data-title="Lukas1" data-content="
            Jan. 3, 2025, 2:05 p.m.
            " data-original-title="" title="">
            Lukas1
         </td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-06 00:00:00+00:00" data-content="Lukas1
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-07 00:00:00+00:00" data-content="Lukas1
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-ffe800 fa fa-question"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-08 00:00:00+00:00" data-content="Lukas1
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-B0E fa fa-thumbs-down"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-09 00:00:00+00:00" data-content="Lukas1
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-10 00:00:00+00:00" data-content="Lukas1
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="noprint vote-actions"><a href="/poll/DMUxeW4VKT/vote/323143/edit/" class="btn btn-xs btn-default" title="Edit vote"><i class="fa fa-pencil"></i></a></td>
      </tr>
      <tr class="vote ">
         <td class="author" data-toggle="popover" data-trigger="hover" data-container="body" data-title="Lukas2" data-content="
            Jan. 3, 2025, 2:05 p.m.
            " data-original-title="" title="">
            Lukas2
         </td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-06 00:00:00+00:00" data-content="Lukas2
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-ffe800 fa fa-question"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-07 00:00:00+00:00" data-content="Lukas2
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-ffe800 fa fa-question"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-08 00:00:00+00:00" data-content="Lukas2
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-09 00:00:00+00:00" data-content="Lukas2
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-10 00:00:00+00:00" data-content="Lukas2
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="noprint vote-actions"><a href="/poll/DMUxeW4VKT/vote/323144/edit/" class="btn btn-xs btn-default" title="Edit vote"><i class="fa fa-pencil"></i></a></td>
      </tr>
      <tr class="vote ">
         <td class="author" data-toggle="popover" data-trigger="hover" data-container="body" data-title="Lukas3" data-content="
            Jan. 5, 2025, 11:42 a.m.
            " data-original-title="" title="">
            Lukas3
         </td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-06 00:00:00+00:00" data-content="Lukas3
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-07 00:00:00+00:00" data-content="Lukas3
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-08 00:00:00+00:00" data-content="Lukas3
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-09 00:00:00+00:00" data-content="Lukas3
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-10 00:00:00+00:00" data-content="Lukas3
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="noprint vote-actions"><a href="/poll/DMUxeW4VKT/vote/323703/edit/" class="btn btn-xs btn-default" title="Edit vote"><i class="fa fa-pencil"></i></a></td>
      </tr>
      <tr class="vote ">
         <td class="author" data-toggle="popover" data-trigger="hover" data-container="body" data-title="Lukas4" data-content="
            Jan. 5, 2025, 11:42 a.m.
            " data-original-title="" title="">
            Lukas4
         </td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-06 00:00:00+00:00" data-content="Lukas4
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-B0E fa fa-thumbs-down"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-07 00:00:00+00:00" data-content="Lukas4
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-08 00:00:00+00:00" data-content="Lukas4
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-B0E fa fa-thumbs-down"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-09 00:00:00+00:00" data-content="Lukas4
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-10 00:00:00+00:00" data-content="Lukas4
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-B0E fa fa-thumbs-down"></span></td>
         <td class="noprint vote-actions"><a href="/poll/DMUxeW4VKT/vote/323704/edit/" class="btn btn-xs btn-default" title="Edit vote"><i class="fa fa-pencil"></i></a></td>
      </tr>
      <tr class="vote ">
         <td class="author" data-toggle="popover" data-trigger="hover" data-container="body" data-title="Lukas6" data-content="
            Jan. 5, 2025, 11:42 a.m.
            " data-original-title="" title="">
            Lukas6
         </td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-06 00:00:00+00:00" data-content="Lukas6
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-07 00:00:00+00:00" data-content="Lukas6
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-08 00:00:00+00:00" data-content="Lukas6
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-09 00:00:00+00:00" data-content="Lukas6
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-90db46 fa fa-check"></span></td>
         <td class="vote-choice text-center
            " data-toggle="popover" data-trigger="hover" data-container="body" data-title="2023-01-10 00:00:00+00:00" data-content="Lukas6
            " data-placement="bottom" data-choice-value="" data-original-title="" title=""><span class="bg-c43131 fa fa-ban"></span></td>
         <td class="noprint vote-actions"><a href="/poll/DMUxeW4VKT/vote/323705/edit/" class="btn btn-xs btn-default" title="Edit vote"><i class="fa fa-pencil"></i></a></td>
      </tr>
   </tbody>
</table>
        """,
    )


def create_no_event_found_endpoints(rsps: responses.RequestsMock, poll_id: str):
    rsps.add(
        responses.GET,
        f"https://bitpoll.de/poll/{poll_id}",
        body="""
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
                            <div class="value">2<span class="fa fa-check"></span></div>
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
        </html>""",
    )
