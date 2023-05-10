import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()

@app.post("/api/v1/users")
async def register_user(
    user: _schemas.UserRequest, db: _orm.Session = _fastapi.Depends(_services.get_db())
):
    db_user = await _services.getUserByEmail(email=user.email,db=db)

    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email ready exist")