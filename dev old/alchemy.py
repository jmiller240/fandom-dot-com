

import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, select, text

# Engine
dbEngine = sqlalchemy.create_engine('sqlite:///fandom_db.db')

with dbEngine.connect() as c:
    results = c.execute(text('select * from account;')).fetchall()    
    print(results)


# Models
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    
    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', email='{self.username}')>"

Base.metadata.create_all(dbEngine)


Session = sessionmaker(bind=dbEngine)
session = Session()
# new_user = Account(name='Bob', email='bob@example.com')
# session.add(new_user)
# session.commit()
retrieved_user = session.query(Account).first()
print(retrieved_user)
session.close()

