from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from schafkopf.api.models import SubscribeRequest, SubscribeResponse, PollResponse, SubscribeCountResponse
from schafkopf.core.dynamodb import email_table, poll_table

app = FastAPI(
    title="Schafkopf Scheduler API",
    openapi_version="3.0.0",
    description="",
)


@app.post("/subscribe")
def subscribe_to_schafkopf_rounds(req: SubscribeRequest) ->SubscribeResponse:
    import boto3
    dynamodb = boto3.resource("dynamodb")
    email_table.add(dynamodb, req.to_email_item())
    return SubscribeResponse(email=req.email)


@app.get("/subscribers/count")
def get_subscriber_count() -> SubscribeCountResponse:
    import boto3
    dynamodb = boto3.resource("dynamodb")
    return SubscribeCountResponse(
        count=email_table.count(dynamodb)
    )

@app.get("/poll")
def get_poll() -> PollResponse:
    import boto3
    dynamodb = boto3.resource("dynamodb")
    poll_item = poll_table.load(dynamodb)
    return PollResponse.from_item(poll_item)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://schafkopf.lukas-bernhard.de",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("schafkopf.api.api:app", port=8000, log_level="info", reload=True)