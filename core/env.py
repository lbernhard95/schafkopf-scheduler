import os
from pathlib import Path

import dotenv
from pydantic import BaseModel, Field


class BaseEnvironment(BaseModel):
    read_only: bool = Field(default=False, alias="READ_ONLY")
    on_aws: bool = Field(default=False, alias="AWS_LAMBDA_FUNCTION_NAME")

    def write_folder(self) -> Path:
        if self.on_aws:
            return Path("/tmp")
        local_folder = Path(__file__).parent.parent / "data"
        if not local_folder.exists():
            local_folder.mkdir(parents=True)
        return local_folder

    @classmethod
    def load(cls) -> "BaseEnvironment":
        dotenv.load_dotenv()
        return cls(**os.environ)
