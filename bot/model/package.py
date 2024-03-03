from .base import Base, UserPackage
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, String, text
from typing import Optional

class Package(Base):

    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
    name: Mapped[str]
    words_count: Mapped[int] = mapped_column(onupdate=text("SELECT COUNT(*) FROM packages"), default=0)
    language: Mapped[Optional[str]]

    users = relationship("User", secondary=UserPackage, back_populates="packages")
