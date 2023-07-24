from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from gpyt_commandbus.model.base import Base

if TYPE_CHECKING:
    from gpyt_commandbus.model.target import Target  # noqa: F401


class Command(Base):
    __tablename__ = "command"

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    target_name = Column(String, ForeignKey("target.name"))
    target = relationship("Target", back_populates="commands")

    def get_JSON(self):  # pylint: disable=invalid-name
        return {
            "id": self.id,
            "data": self.data,
            "timestamp": str(self.timestamp),
            "target_name": self.target_name,
        }
