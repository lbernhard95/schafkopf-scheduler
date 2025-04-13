import os
from pathlib import Path

import dotenv
from pydantic import BaseModel, Field


class BaseEnvironment(BaseModel):
    read_only: bool = Field(default=False, alias="READ_ONLY")
    lambda_name: str = Field(default="", alias="RUNNING_ON_AWS")

    def write_folder(self) -> Path:
        if self.on_aws:
            return Path("/tmp")
        local_folder = Path(__file__).parent.parent / "data"
        if not local_folder.exists():
            local_folder.mkdir(parents=True)
        return local_folder

    @property
    def on_aws(self) -> bool:
        return bool(self.lambda_name)

    @classmethod
    def load(cls) -> "BaseEnvironment":
        dotenv.load_dotenv()
        return cls(**os.environ)
