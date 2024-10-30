from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI(
    title="Schafkopf Scheduler API",
    openapi_version="3.0.0",
    description="",
)


@app.get(
    "/"
)
def hello() -> str:
    return "Hello World"


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)