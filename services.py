import database as _database
import models as _models
import sqlalchemy.orm as _orm
import schemas as _schemas
import email_validator as _email_validator
import fastapi as _fastapi
import passlib.hash as _hash
import jwt as _jwt

_JWT_SECRET = "fdsfdsfdsf"


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db= _database.SessionLocal()

    try:
        yield db
    finally:
        db.close()    

async def getUserByEmail(email: str, db: _orm.Session):
    return db.query(_models.UserModel).filter(_models.UserModel.email == email).first()


async def create_user(user: _schemas.UserRequest, db: _orm.Session):
    try:
        isValid = _email_validator.validate_email(email=user.email)
        email = isValid.email
    except _email_validator.EmailNotValidError as e:
        raise _fastapi.HTTPException(status_code=404,detail="invalid email")
    
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.UserModel(
        email=email,
        name=user.name,
        phone=user.phone,
        password_hash=hashed_password
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def create_token(user: _models.UserModel):
    user_schema = _schemas.UserResponse.from_orm(user)
    print(user_schema)
    user_dict = user_schema.dict()
    del user_dict["created_at"]

    token = _jwt.encode(user_dict,_JWT_SECRET)

    return dict(access_token = token, token_type = "brearer")


async def login(email:str,password:str, db: _orm.Session):
    db_user = await getUserByEmail(email=email,db=db)
    
    if not db_user:
        return False
    
    if not db_user.password_verification(password=password):
        return False
    
    return db_user