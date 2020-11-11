from datetime import datetime, date, time


import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def valid_email(email):
    if len(email) < 5 or '@' not in email or '.' not in email or email.endswith('.'):
        return False
    else:
        domain = email.split('@')[1]
        if not domain:
            return False
        else:
            x = email.count("@")
            y = domain.count(".")
            if x != 1 or y < 1:
                return False
            else:
                return True


def request_data():
    print("Госпожа спортсменка/господин спортсмен, позвольте записать ваши данные!")
    first_name = input("Ваше имя: ")
    last_name = input("Ваша фамилия: ")
    gender = input("Пол: 1 - Female, 2 - Male: ")
    if gender == '1':
        gender = 'Female'
    elif gender == '2':
        gender = 'Male'
    else:
        print('Есть только два гендера!')
    email = input('Введите адрес электронной почты: ')
    birthdate = date(int(input('Год рождения: ')), int(input('Месяц: ')), int(input("Число: ")))
    height = input("Укажите ваш рост: ")
    if valid_email(email):
        user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            birthdate=birthdate,
            height=height
        )

        return user


def main():
    session = connect_db()
    user = request_data()
    if user:
        session.add(user)
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print('Неправильный формат email')


if __name__ == "__main__":
    main()
