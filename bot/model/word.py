from .base import Base
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import Optional, List

class Word(Base):

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
    value: Mapped[str] = mapped_column(String[50])
    translate: Mapped[str] = mapped_column(String[50])
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"))
    additional_info: Mapped[Optional[str]]

    user_words: Mapped[Optional[List["UserWord"]]] = relationship("UserWord", back_populates="word")


class UserWord(Base):

    __tablename__ = "user_words"
    
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, unique=True, primary_key=True)
    level: Mapped[int] = mapped_column(default=1)
    last_repetition_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="words") # noqa: F821
    word: Mapped["Word"] = relationship("Word", back_populates="user_words")
