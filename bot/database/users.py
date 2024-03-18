from bot.common import session
from bot.model import User, Package, UserWord


# проверяеть есть ли пользователь в базе данных 
def user_exist(vkid: int) -> bool:
    return bool(session.query(User).filter(User.vkid == vkid).first())

# добавляет пользователя в базу данных 
def add_user(vkid: int, name: str) -> User:
    user = User(vkid=vkid, name=name)
    session.add(user)
    session.flush()

# возвращает пользователя по идентификатору в вк
def get_user_by_vkid(vkid: int) -> User | None:
    return session.query(User).filter(User.vkid == vkid).first()

# возвращает пользователя по внутреннему идентификатору 
def get_user_by_id(id: int) -> User | None:
    return session.query(User).filter(User.id == id).first()

# добавляет пакет для пользователя
def add_package_to_user(user: User, package: Package):
    user.packages.append(package)
    session.flush()
# удаляет пакет в пользователя 
def delete_package_from_user(package_id: int, user: User) -> Package | None:
    package = session.query(Package).filter(Package.id == package_id).first()
    user.packages.remove(package)
    session.flush()
    return package
# проверяет выполненил ли пользователь дневную цель для изучения 
def user_complete_day_goal(user: User) -> bool:
    if user.day_deep_repetition < user.day_goal * 2 or user.day_fast_repetition < user.day_goal * 2 or user.day_new < user.day_goal:
        return False
    return True
# возвращает количество слов изученных пользователем
def get_user_words_count(user: User) -> int:
    return session.query(UserWord).filter(UserWord.user_id == user.id).count()