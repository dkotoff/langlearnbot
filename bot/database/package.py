import random
from bot.model import Package, User, UserPackage
from typing import List
from bot.common import session

#возвращает список всех пакетов в БД
def get_all_packages() -> List[Package] | None:
    return session.query(Package).all()

#возвращает активен ли пакет у пользователя 
def package_user_active(user_id: int, package_id: int) -> bool:
    return bool(session.query(UserPackage).filter(UserPackage.c.package_id == package_id, UserPackage.c.user_id == user_id).first())

# возвращает пакет по его идентификатору
def get_package_by_id(id: int) -> Package | None:
    return session.query(Package).filter(Package.id == id).first()

# возвращает случайный пакет у пользователя 
def get_user_random_packge(user: User):
    count = len(user.packages)
    rnum = random.randint(0, count-1)

    return user.packages[rnum]

# возвращает все пакеты пользователя
def get_user_packages(user: User) -> List[Package]:
    return user.packages