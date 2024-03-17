from .base import Base, UserPackage
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from typing import List, Optional

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
    vkid: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[Optional[str]]
    notification: Mapped[Optional[str]] = mapped_column(default="выкл.")
    day_goal: Mapped[int] = mapped_column(Integer, default=0)
    day_new: Mapped[int] = mapped_column(default=0)
    day_fast_repetition: Mapped[int] = mapped_column(default=0)
    day_deep_repetition: Mapped[int] = mapped_column(default=0)
    packages: Mapped[List["Package"]] = relationship("Package", secondary=UserPackage, back_populates="users")  # noqa: F821
    words: Mapped[List["UserWord"]] = relationship("UserWord", back_populates="user")    # noqa: F821
