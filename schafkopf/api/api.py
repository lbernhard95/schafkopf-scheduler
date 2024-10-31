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
        "https://schafkopf.lukas-bernhard.de",  # your frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("schafkopf.api.api:app", port=8000, log_level="info", reload=True)