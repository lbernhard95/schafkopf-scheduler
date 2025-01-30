from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

from schafkopf.core import bitpoll
from tests.unit.resources import resources


class TestParseVotes:
    def test_parse_from_html(self):
        table = resources.load_bitpoll_table_html()

        votes = bitpoll.parse_votes(BeautifulSoup(table))

        pd.testing.assert_frame_equal(
            votes,
            pd.DataFrame(
                [
                    {"date": "2025-01-06", "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas1", "vote": "fa-question"},
                    {"date": "2025-01-08", "user": "Lukas1", "vote": "fa-thumbs-down"},
                    {"date": "2025-01-10", "user": "Lukas1", "vote": "fa-ban"},
                    {"date": "2025-01-06", "user": "Lukas2", "vote": "fa-question"},
                    {"date": "2025-01-07", "user": "Lukas2", "vote": "fa-question"},
                    {"date": "2025-01-08", "user": "Lukas2", "vote": "fa-check"},
                    {"date": "2025-01-09", "user": "Lukas2", "vote": "fa-check"},
                    {"date": "2025-01-10", "user": "Lukas2", "vote": "fa-ban"},
                ]
            ),
        )


class TestFindDayForNextEvent:
    def test_no_perfect_day_found(self):
        day = bitpoll.find_day_for_next_event(
            pd.DataFrame(
                [
                    {"date": "2025-01-06", "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas2", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas3", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas4", "vote": "fa-question"},
                    {"date": "2025-01-07", "user": "Lukas2", "vote": "fa-question"},
                    {"date": "2025-01-07", "user": "Lukas3", "vote": "fa-thumbs-down"},
                    {"date": "2025-01-07", "user": "Lukas4", "vote": "fa-ban"},
                ]
            )
        )
        assert day is None

    def test_only_one_day_with_four_votes(self):
        match_day = "2025-01-07"
        day = bitpoll.find_day_for_next_event(
            pd.DataFrame(
                [
                    {"date": match_day, "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas2", "vote": "fa-question"},
                    {"date": match_day, "user": "Lukas3", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas3", "vote": "fa-thumbs-down"},
                    {"date": match_day, "user": "Lukas4", "vote": "fa-check"},
                    {"date": "2025-01-06", "user": "Lukas4", "vote": "fa-ban"},
                    {"date": match_day, "user": "Lukas2", "vote": "fa-check"},
                ]
            )
        )

        assert day == datetime(2025, 1, 7, 18, 30)

    def test_match_is_selected_based_on_probability(self):
        high_prop_day = "2025-01-06"
        day = bitpoll.find_day_for_next_event(
            pd.DataFrame(
                [
                    {"date": high_prop_day, "user": "Lukas1", "vote": "fa-check"},
                    {"date": high_prop_day, "user": "Lukas2", "vote": "fa-check"},
                    {"date": high_prop_day, "user": "Lukas3", "vote": "fa-check"},
                    {"date": high_prop_day, "user": "Lukas4", "vote": "fa-check"},
                    {"date": high_prop_day, "user": "Lukas5", "vote": "fa-question"},
                    {"date": "2025-01-07", "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas2", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas3", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas4", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas5", "vote": "fa-thumbs-down"},
                ]
            )
        )
        assert day == datetime(2025, 1, 6, 18, 30)


class TestGetListOfAttandees:
    def test_get_correct_names_from_date_and_vote(self):
        day = "2025-01-06"
        result = bitpoll.get_list_of_attendees(
            pd.DataFrame(
                [
                    {"date": "2025-01-05", "user": "Lukas1", "vote": "fa-check"},
                    {"date": "2025-01-05", "user": "Lukas2", "vote": "fa-check"},
                    {"date": day, "user": "Lukas1", "vote": "fa-check"},
                    {"date": day, "user": "Lukas2", "vote": "fa-question"},
                    {"date": day, "user": "Lukas3", "vote": "fa-check"},
                    {"date": "2025-01-07", "user": "Lukas1", "vote": "fa-check"},
                ]
            ),
            date=day,
        )

        assert result == ["Lukas1", "Lukas3"]
