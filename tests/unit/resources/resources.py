import os

RESOURCE_FOLDER_PATH = f"{os.path.dirname(os.path.abspath(__file__))}"

def load_bitpoll_table_html() -> str:
    with open(f"{RESOURCE_FOLDER_PATH}/bitpoll_table.html", "r") as f:
        return f.read()