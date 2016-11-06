
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from jizera import app

db_location = '/tmp/jizera-testing.db'

engine = create_engine('sqlite:///' + db_location, convert_unicode=True, echo=app.debug)
dbsession = scoped_session(sessionmaker(bind=engine,autocommit=False))

Base = declarative_base()
Base.query = dbsession.query_property()

def init_db():
    import jizera.models
    Base.metadata.create_all(bind=engine)

def destroy_db():
    dbsession.remove()
