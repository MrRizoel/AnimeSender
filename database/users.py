from sqlalchemy import Column, BigInteger
from . import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(BigInteger, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

Users.__table__.create(checkfirst=True)

def adduser(user_id):
   Check = SESSION.query(Users).get(int(user_id))
   if not Check:
      SESSION.add(Users(user_id))
      SESSION.commit()
   else:
      SESSION.close()

def count():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()

def get_all_users():
    try:
        return SESSION.query(Users).all()
    finally:
        SESSION.close()
