from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from gpyt_commandbus.model.base import Base

if TYPE_CHECKING:
    from gpyt_commandbus.model.command import Command  # noqa: F401


class Target(Base):
    __tablename__ = "target"

    url = Column(String(255), nullable=False)
    name = Column(String(255), primary_key=True)
    commands = relationship(
        "Command", back_populates="target"
    )
