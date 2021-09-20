# backend for wat_do

from sqlalchemy import create_engine, Column, String, Date, Time, Integer
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


db_string = "postgresql://postgres:pg@localhost:5432/wat_do"
base = declarative_base()


class Activity(base):
    __tablename__ = 'activities'

    name = Column(String)
    sub_activity = Column(String)
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.now())
    time = Column(Time, default=datetime.now())
    duration = Column(Integer) # seconds

    def __repr__(self):
        return f"activity(id={self.id!r}, name={self.name!r}, sub_activity={self.sub_activity!r}, date={self.date}, duration={self.duration})"

engine = create_engine(db_string, echo=False, future=True)
sm = sessionmaker(engine)
session = sm()
base.metadata.create_all(engine)    


def add_activity(name, sub_activity, duration):
    session.add(Activity(name=name, sub_activity=sub_activity, duration=duration))
    session.commit()

def get_all_activities():
    return session.query(Activity)

def get_activity_history_by_name(name):
    return session.query(Activity).\
        filter(Activity.name == name).\
        order_by(Activity.sub_activity).\
        order_by(Activity.date)

def get_activity_history_in_past_days(days):
    x_days_ago = datetime.now() - timedelta(days=days)
    return session.query(Activity).\
        filter(Activity.date >= x_days_ago)

def delete_by_id(id):
    act = session.get(Activity, id)
    session.delete(act)
    session.commit()
