from bot.common import session
from bot.model import User, Package, UserWord


def user_exist(vkid: int) -> bool:
    return bool(session.query(User).filter(User.vkid == vkid).first())

def add_user(vkid: int, name: str) -> User:
    user = User(vkid=vkid, name=name)
    session.add(user)
    session.flush()


def get_user_by_vkid(vkid: int) -> User | None:
    return session.query(User).filter(User.vkid == vkid).first()

def get_user_by_id(id: int) -> User | None:
    return session.query(User).filter(User.id == id).first()


def add_package_to_user(user: User, package: Package):
    user.packages.append(package)
    session.flush()

def delete_package_from_user(package_id: int, user: User) -> Package | None:
    package = session.query(Package).filter(Package.id == package_id).first()
    user.packages.remove(package)
    session.flush()
    return package

def user_complete_day_goal(user: User) -> bool:
    if user.day_deep_repetition < user.day_goal * 2 or user.day_fast_repetition < user.day_goal * 2 or user.day_new < user.day_goal:
        return False
    return True

def get_user_words_count(user: User) -> int:
    return session.query(UserWord).filter(UserWord.user_id == user.id).count()