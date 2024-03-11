from bot.common import session
import random
from bot.model import User, Word, Package, UserWord 
from sqlalchemy import and_

def get_random_word_from_package_with_no_user(package: Package, user: User) -> Word | None:
    count = (session.query(Word)
    .join(UserWord, and_(Word.id == UserWord.word_id, UserWord.user_id == user.id), isouter=True)
    .filter(and_(Word.package_id == package.id, UserWord.id == None)).count())

    rnum = random.randint(0, count-1)

    word = (session.query(Word)
    .join(UserWord, and_(Word.id == UserWord.word_id, UserWord.user_id == user.id), isouter=True)
    .filter(and_(Word.package_id == package.id, UserWord.id == None))
    .offset(rnum).limit(1).first())
    
    return word

def get_random_userword_by_level(user: User, level: int) -> UserWord | None:
    count = session.query(UserWord).filter(and_(UserWord.user_id == user.id, UserWord.level == level)).count()

    rnum = random.randint(0, count)

    return (session.query(UserWord)
            .filter(and_(UserWord.user_id == user.id, UserWord.level == level))
            .offset(rnum).limit(1).first())


def add_word_to_user(word: Word, user: User) -> UserWord:
    user_word = UserWord(word_id = word.id, user_id = user.id)
    session.add(user_word)   
    session.flush()
    return user_word
