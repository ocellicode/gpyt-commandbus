from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommandModel(BaseModel):
    data: dict
    target_name: str
    id: Optional[int] = None
    timestamp: datetime = datetime.utcnow()
