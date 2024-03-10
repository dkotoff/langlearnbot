import random
from bot.database.word import get_random_userword_by_level, get_random_word_from_package_with_no_user, add_word_to_user
from bot.database.package import get_user_random_packge
from bot.database.users import user_complete_day_goal
from typing import Tuple
from bot.model import UserWord, User
from bot.common import session


def random_category() -> int:
    rnum = random.randint(0, 100)
    if 85 < rnum <= 100:
        return 0
    elif 50 < rnum <= 85:
        return 1
    elif 25 < rnum <= 50:
        return 2
    elif 8 < rnum <= 25:
        return 3
    elif 0 <= rnum <= 8:
        return 4

def get_random_word(user: User) -> Tuple[UserWord, int]:
    category = random_category()
    package = get_user_random_packge(user)

    while True:
        if category == 0:
            word = get_random_word_from_package_with_no_user(user=user, package=package)
            if not word:
                category+=1
                continue
            word = add_word_to_user(word, user)
            session.commit()
            break
        elif 1 <= category <= 4:
            word = get_random_userword_by_level(user=user, level=category)
            if not word:
                category+=1
                continue
            break
        else:
            category = 0
            continue
    return word, category

def get_daily_word(user: User) -> Tuple[UserWord, int]:
    package = get_user_random_packge(user)
    category = 0

    if user.day_new < user.day_goal:
        word = get_random_word_from_package_with_no_user(package, user)
        category = 0
        user.day_new += 1
        session.commit()
    elif user.day_fast_repetition < user.day_goal * 2:
        while True:
            word = get_random_userword_by_level(user=user, level=1)
            category = 1
            if word:
                break
            word = get_random_userword_by_level(user=user, level=2)
            category = 2
            if word: 
                break
            word = None
            break
        user.day_fast_repetition += 1
        session.commit()
    elif user.day_deep_repetition < user.day_goal * 2:
        while True:
            word = get_random_userword_by_level(user=user, level=3)
            category = 3
            if word:
                break
            word = get_random_userword_by_level(user=user, level=4)
            category = 4
            if word: 
                break
            word = None
            break
        user.day_deep_repetition += 1
        session.commit()
    else: 
        word, category = None, 0
    return word, category
        

def get_word(user: User) -> Tuple[UserWord, int]:
    print("11\n\n")
    if not user_complete_day_goal(user):
        word, category = get_daily_word(user)
        if not word:
            return get_random_word(user)
        
    else:
        return get_random_word(user)

    return word, category