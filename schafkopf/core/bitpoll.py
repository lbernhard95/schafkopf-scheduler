import re
from datetime import datetime
from typing import List, Optional

import bs4
import pandas as pd
from pydantic import BaseModel, computed_field
import requests
from bs4 import BeautifulSoup

BITPOLL_URL = "https://bitpoll.de"


class VoteDayResult(BaseModel):
    date: datetime
    yes_count: int
    no_count: int
    probably_yes_count: int
    probably_no_count: int

    @computed_field
    @property
    def attendance_probability(self) -> float:
        return (
            self.yes_count * 100 + self.no_count * 0 + self.probably_no_count * 25 + self.probably_yes_count * 50
        ) / self.participation_count

    @computed_field
    @property
    def participation_count(self) -> int:
        return self.yes_count + self.no_count + self.probably_no_count + self.probably_yes_count


def get_voting_table(poll_id: str) -> bs4.Tag:
    rsp = requests.get(get_website_from_poll_id(poll_id))
    page = BeautifulSoup(rsp.text, features="html.parser")
    return page.find("table", id="poll")


def parse_votes(table: bs4.Tag) -> pd.DataFrame:
    votes = []
    for row in table.select("tr.vote"):
        user = row.select_one("td.author").get_text(strip=True)
        for cell in row.select("td.vote-choice"):
            try:
                date = cell["data-title"].split()[0]  # Extract only the date part
                vote_icon = cell.select_one("span.fa")
                if vote_icon:
                    vote_type = vote_icon["class"][2]  # Assuming format like 'fa fa-check'
                    votes.append({"date": date, "user": user, "vote": vote_type})
            except Exception:
                print(f"Error parsing vote for user {user}")
    return pd.DataFrame(votes)


def find_day_for_next_event(df: pd.DataFrame) -> Optional[datetime]:
    vote_weights = {
        "fa-check": 100,
        "fa-ban": 0,
        "fa-question": 50,
        "fa-thumbs-down": 25,
    }

    # Group by date and calculate the required metrics
    grouped = (
        df.groupby("date")
        .agg(
            yes_count=("vote", lambda x: (x == "fa-check").sum()),
            attendance_probability=(
                "vote",
                lambda x: sum(vote_weights[v] for v in x) / len(x),
            ),
        )
        .reset_index()
    )

    # Filter dates with at least 4 "fa-check" votes
    filtered = grouped[grouped["yes_count"] >= 4]

    # Select the date with the highest attendance probability
    if filtered.empty:
        return None
    best_day = filtered.loc[filtered["attendance_probability"].idxmax()]["date"]
    return datetime.strptime(best_day, "%Y-%m-%d").replace(hour=18, minute=30)


def get_list_of_attendees(df: pd.DataFrame, date: datetime) -> List[str]:
    return df[(df["date"] == str(pd.to_datetime(date).date())) & (df["vote"] == "fa-check")]["user"].tolist()


def create_new_poll(csrf_token: str):
    data = {
        "csrfmiddlewaretoken": csrf_token,
        "type": "date",
        "title": "[at] Schafkopfen",
        "random_slug": "random_slug",
        "due_date": "",
        "description": "",
        "anonymous_allowed": "on",
        "one_vote_per_user": "on",
    }

    response = requests.post(f"{BITPOLL_URL}/", headers=get_headers(csrf_token), data=data)

    if response.status_code != 200:
        raise ValueError(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    edit_path = soup.find("a", {"data-shortcut": "g c"})["href"]
    poll_id = re.search(r"/poll/([^/]+)/edit/choices/", edit_path).group(1)
    return poll_id


def get_valid_csrf_token() -> str:
    response = requests.get(f"{BITPOLL_URL}/", headers=get_headers(None))
    response.raise_for_status()  # Ensure the request was successful

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
    return csrf_token


def add_choices_to_poll(poll_id: str, csrf_token: str, dates: List[datetime]):
    data = {
        "csrfmiddlewaretoken": csrf_token,
        "dates": ",".join([d.strftime("%Y-%m-%d") for d in dates]),
    }
    response = requests.post(
        f"{get_website_from_poll_id(poll_id)}/edit/choices/date/",
        headers=get_headers(csrf_token),
        data=data,
    )

    if response.status_code != 200:
        raise ValueError(response.text)


def get_website_from_poll_id(poll_id: str) -> str:
    return f"{BITPOLL_URL}/poll/{poll_id}"


def get_headers(csrf_token: Optional[str]) -> {}:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://bitpoll.de/",
        "Cookie": f"csrftoken = {csrf_token}" if csrf_token else "",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://bitpoll.de",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "TE": "trailers",
    }
