import os

import dotenv
from pydantic import BaseModel, Field


class BaseEnvironment(BaseModel):
    read_only: bool = Field(default=False, alias="READ_ONLY")

    @classmethod
    def load(cls) -> "BaseEnvironment":
        dotenv.load_dotenv()
        return cls(**os.environ)
