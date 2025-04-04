def load_html_template(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        return f.read()
