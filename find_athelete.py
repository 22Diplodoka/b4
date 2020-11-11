import datetime
from datetime import datetime, date

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

    def __repr__(self):
        return f'Ближайший по росту спортсмен: {self.name} - {self.height} '


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def main():
    session = connect_db()
    users = session.query(User)
    users_id = session.query(User.id)
    user_ids = [user.id for user in users.all()]
    user_hs = [user.height for user in users.all()]

    id_inp = int(input('Введите id зарегистрированного участника: '))
    print('Имя спортсмена: ', session.query(User.name).filter(User.id == id_inp).first()[0])

    if id_inp in user_ids:
        for i in user_ids:
            if i == id_inp:
                uid = datetime.strptime(session.query(User.birthdate).filter(User.id == id_inp).first()[0], "%Y-%m-%d")
                uih = session.query(User.height).filter(User.id == id_inp).first()[0]
                if uih is not None:
                    for h in range(len(user_hs)):
                        if user_hs[h] is None:
                            user_hs[h] = 0.0
                    user_h = []
                    for x in map(lambda h: abs(h - uih), user_hs):
                        user_h.append(x)
                    uh_dict = dict(zip(user_ids, user_h))
                    del uh_dict[users_id.filter(User.id == id_inp).first()[0]]
                    for key, val in uh_dict.items():
                        if uh_dict[key] == min(uh_dict.values()):
                            nearest_height = users.filter(User.id == key).first()
                            print(nearest_height)
                            break
                else:
                    print('Данные о росте не внесены в базу')

                user_bs = [datetime.strptime(user.birthdate, "%Y-%m-%d") for user in users.all()]

                us_bs = []
                for x in map(lambda b: abs(uid - b), user_bs):
                    us_bs.append(x)

                us_dict = dict(zip(user_ids, us_bs))
                del us_dict[users_id.filter(User.id == id_inp).first()[0]]
                for key, val in us_dict.items():
                    if us_dict[key] == min(us_dict.values()):
                        nearest_birth = users.filter(User.id == key).first()
                        print('Ближайший по дате рождения спортсмен: ', nearest_birth.name, '-', nearest_birth.birthdate)
                        break

    elif id_inp not in user_ids:
        print('Пользователя с таким id нет=(((')

    session.close()


if __name__ == "__main__":
    main()