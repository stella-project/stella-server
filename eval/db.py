from sqlalchemy import create_engine, MetaData, Table, and_

DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'

engine = create_engine(DATABASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)
users = Table('users', metadata, autoload=True)
systems = Table('systems', metadata, autoload=True)
sessions = Table('sessions', metadata, autoload=True)
feedbacks = Table('feedbacks', metadata, autoload=True)
results = Table('results', metadata, autoload=True)
roles = Table('roles', metadata, autoload=True)
