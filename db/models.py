from sqlalchemy import Column, Integer, BigInteger, String, Text

from db.base import Base


class PlayerBalance(Base):
    __tablename__ = 'playerbase'

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(100))
    balance = Column(Integer, default=50)
