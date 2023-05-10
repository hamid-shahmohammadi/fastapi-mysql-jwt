import sqlalchemy as sqlalchemy
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DB_URL = "mysql+pymysql://root:@localhost/fastapi_jwt?charset=utf8mb4"
engine = sqlalchemy.create_engine(DB_URL)

SessionLocal = orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative.declarative_base()