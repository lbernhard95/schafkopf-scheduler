from pydantic import Field

from core.env import BaseEnvironment


class Environment(BaseEnvironment):
    zhs_username: str = Field(alias="ZHS_USERNAME")
    zhs_password: str = Field(alias="ZHS_PASSWORD")
