import random
from bot.model import Package, User, UserPackage
from typing import List
from sqlalchemy import text
from bot.common import session

def get_all_packages() -> List[Package] | None:
    return session.query(Package).all()

def package_user_active(user_id: int, package_id: int) -> bool:
    return bool(session.query(UserPackage).filter(UserPackage.c.package_id == package_id, UserPackage.c.user_id == user_id).first())

def get_package_by_id(id: int) -> Package | None:
    return session.query(Package).filter(Package.id == id).first()

def get_user_random_packge(user: User):
    count = len(user.packages)
    rnum = random.randint(0, count-1)

    return user.packages[rnum]