from bot.database.word import get_random_userword_by_level, get_random_word_from_package_with_no_user, add_word_to_user
from bot.database.package import get_user_random_packge
from bot.database.users import user_complete_day_goal
from typing import Tuple
from bot.model import UserWord, User
from bot.common import session
import logging


def get_random_word(user: User) -> Tuple[UserWord, int]:
    category = 1
    logging.info("random trigger")
    while True:
            word = get_random_userword_by_level(user=user, level=category)
            if not word:
                category+=1
                if category > 10:
                    break    
                continue
                
            break
    return word, category

def get_daily_word(user: User) -> Tuple[UserWord, int]:
    category = 0
    package = get_user_random_packge(user)
    word = None
    g = user.day_goal 

    if user.day_new < g:
        word = get_random_word_from_package_with_no_user(package, user)
        if word:
            word = add_word_to_user(word, user)
            return word, category
        category +=1

    elif user.day_fast_repetition < g*2:
        category = 1
        while category < 3:
            word = get_random_userword_by_level(user, category)
            if word:
                return word, category
            category += 1

    elif user.day_deep_repetition < g*2:
        category = 3
        while category < 5:
            word = get_random_userword_by_level(user, category)
            if word:
                return word, category
            category += 1

    return word, category

def add_point_to_user_category(user: User, category: int) -> None:
    if category == 0:
        user.day_new += 1
    elif category in [1, 2]:
        user.day_fast_repetition += 1
    else:
        user.day_deep_repetition += 1 


def get_word(user: User) -> Tuple[UserWord, int]:
    word, category = None, 0
    if not user_complete_day_goal(user):
        word, category = get_daily_word(user)
        
    else:
        word, category = get_random_word(user)

    if not word:
        word, category = get_random_word(user)

    add_point_to_user_category(user, category)
    session.commit()

    return word, category