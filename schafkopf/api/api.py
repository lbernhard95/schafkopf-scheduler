from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from schafkopf.api.models import SubscribeRequest, SubscribeResponse, PollResponse, SubscribeCountResponse
from schafkopf.core import gmail, bitpoll
from schafkopf.core.dynamodb import email_table, poll_table

app = FastAPI(
    title="Schafkopf Scheduler API",
    openapi_version="3.0.0",
    description="",
)


@app.post("/subscribe")
def subscribe_to_schafkopf_rounds(req: SubscribeRequest) -> SubscribeResponse:
    import boto3
    dynamodb = boto3.resource("dynamodb")
    email_item = req.to_email_item()
    email_table.add(dynamodb, email_item)

    poll = poll_table.load(dynamodb)
    poll_id = bitpoll.get_website_from_poll_id(poll.running_poll_id)
    if poll.poll_is_running():
        print("Send invite email with poll link")
        gmail.send_welcome_with_running_bitpoll(
            receiver=req.email,
            bitpoll_link=poll_id,
        )
    else:
        print('Send invite email with next date')
        gmail.send_welcome_with_meeting_invitation(
            receiver=req.email,
            start=poll.next_schafkopf_event,
            bitpoll_link=poll_id
        )
    return SubscribeResponse(email=email_item.email)


@app.delete("/subscriber")
def delete_subscriber_from_mailing_list(email: str) -> SubscribeResponse:
    import boto3
    dynamodb = boto3.resource("dynamodb")
    email_table.delete(dynamodb, email.lower())
    return SubscribeResponse(email=email.lower())


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