from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.db import crud, models
from app.api import dependencies as dep
from app.core import config, security


router = APIRouter()


@router.post('/login/access-token')
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                       db: Session = Depends(dep.get_db)):
    admin = crud.admin.authenticate(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=400, detail="Incorrect username or password.")
