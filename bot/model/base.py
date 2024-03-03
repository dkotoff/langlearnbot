from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Table, Column, ForeignKey

class Base(DeclarativeBase):
    pass

UserPackage = Table("UserPackage", Base.metadata,
                    Column("package_id", ForeignKey("packages.id")),
                    Column("user_id", ForeignKey("users.id")))