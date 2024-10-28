
from datetime import datetime
from typing import List
from uuid import uuid4
from pydantic import BaseModel, computed_field
import requests
from bs4 import BeautifulSoup


BITPOLL_URL = 'https://bitpoll.de'
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://bitpoll.de/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://bitpoll.de',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    'TE': 'trailers',
}

class VoteDate(BaseModel):
    date: datetime
    yes_count: int
    no_count: int
    probably_yes_count: int
    probably_no_count: int

    @staticmethod
    def from_bitpoll_date(date: str) -> "VoteDate":
        return VoteDate(
            date=datetime.strptime(date, "%a, %d. %b. %Y"),
            yes_count=0, 
            no_count=0,
            probably_no_count=0,
            probably_yes_count=0
        )
    
    @computed_field
    @property
    def attendance_probability(self) -> float:
        return (
            self.yes_count * 100 +
            self.no_count * 0 +
            self.probably_no_count * 25 +
            self.probably_yes_count * 50
        ) / self.participation_count

    @computed_field
    @property
    def participation_count(self) -> int:
        return self.yes_count + self.no_count + self.probably_no_count + self.probably_yes_count
    


def get_poll_webpage(poll_id: str) -> BeautifulSoup:
    rsp = requests.get(get_website_from_poll_id(poll_id))
    return BeautifulSoup(rsp.text, features="html.parser")


def collect_vote_dates(poll_page: BeautifulSoup) -> List[VoteDate]:
    dates = [date.get_text(strip=True) for date in poll_page.select("thead th.choice-group")]
    details_row = poll_page.select("tfoot tr.print-only")[1]
    
    all_votes = []
    for i, cell in enumerate(details_row.select("td")):
        votes = VoteDate.from_bitpoll_date(
            date=dates[i]
        )
        
        # Get all 'value' divs in this cell (each represents a vote count for a specific vote type)
        for vote_div in cell.select("div.value"):
            # Extract vote count and vote type
            vote_count = int(vote_div.get_text(strip=True))
            vote_type_icon = vote_div.select_one("span.fa")
            
            if vote_type_icon:
                # Use the class name of the icon to determine the type of vote
                vote_type = vote_type_icon['class'][1]  # Assuming format like 'fa fa-ban'
                # Store the count in the dictionary
                match vote_type:
                    case "fa-ban": 
                        votes.no_count += vote_count
                    case "fa-check":
                        votes.yes_count += vote_count
                    case "fa-question":
                        votes.probably_yes_count += vote_count
                    case "fa-thumbs-down":
                        votes.probably_no_count += vote_count
        all_votes.append(votes)
    return all_votes


def create_new_poll(csrf_token: str):
    poll_id = str(uuid4())

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'type': 'date',
        'title': "[at] Schafkopfen",
        'random_slug': 'random_slug',
        'url': poll_id,
        'due_date': '',
        'description': "",
        'anonymous_allowed': 'on',
        'one_vote_per_user': 'on',
    }

    response = requests.post(f"{BITPOLL_URL}/", headers=BROWSER_HEADERS, data=data)

    if response.status_code != 200:
        raise ValueError(response.text)
    return poll_id


def get_valid_csrf_token() -> str:
    # Start a session to persist cookies across requests
    session = requests.Session()

    # Step 1: Make an initial GET request to the Bitpoll homepage to get the CSRF token
    response = session.get(f"{BITPOLL_URL}/", headers=BROWSER_HEADERS)
    response.raise_for_status()  # Ensure the request was successful

    # Step 2: Parse the HTML to find the CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return csrf_token

def add_choices_to_poll(poll_id: str, csrf_token: str, dates: List[datetime]):
    data = {
        'csrfmiddlewaretoken': csrf_token,
        "dates": ",".join([d.strftime("%Y-%m-%d") for d in dates])
    }
    response = requests.post(f"{get_website_from_poll_id(poll_id)}/edit/choices/date/", headers=BROWSER_HEADERS, data=data)
    
    if response.status_code != 200:
        raise ValueError(response.text)
    

def get_website_from_poll_id(poll_id: str) -> str:
    return f"{BITPOLL_URL}/poll/{poll_id}"