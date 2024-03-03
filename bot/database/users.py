from bot.common import session
from bot.model import User, Package


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