from pydantic import AnyUrl, BaseModel


class TargetModel(BaseModel):
    name: str
    url: AnyUrl
