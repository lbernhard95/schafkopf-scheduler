from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from schafkopf.api.models import SubscribeRequest, SubscribeResponse, PollResponse, SubscribeCountResponse
from schafkopf.boto3.email import EmailTable, SubscriberTable
from schafkopf.boto3.poll import PollTable
from schafkopf.core import gmail

app = FastAPI(
    title="Schafkopf Scheduler API",
    openapi_version="3.0.0",
    description="",
)


@app.post("/subscribe")
def subscribe_to_schafkopf_rounds(req: SubscribeRequest) -> SubscribeResponse:
    sub = req.to_subscriber()
    SubscriberTable().add(sub)

    poll = PollTable().get_current_poll()
    if poll.poll_is_running():
        print("Send invite email with poll link")
        gmail.send_welcome_with_running_bitpoll(
            receiver=req.email,
            bitpoll_link=poll.url,
        )
    else:
        print('Send invite email with next date')
        gmail.send_welcome_with_meeting_invitation(
            receiver=req.email,
            start=poll.upcoming_event,
            bitpoll_link=poll.url
        )
    return SubscribeResponse(email=sub.email)


@app.delete("/subscriber")
def delete_subscriber_from_mailing_list(email: str) -> SubscribeResponse:
    SubscriberTable().delete(email)
    return SubscribeResponse(email=email)


@app.get("/subscribers/count")
def get_subscriber_count() -> SubscribeCountResponse:
    return SubscribeCountResponse(
        count=SubscriberTable().count()
    )

@app.get("/poll")
def get_poll() -> PollResponse:
    poll = PollTable().get_current_poll()
    return PollResponse.from_item(poll)


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