from fastapi import APIRouter

from app.api.routes import login, article


api_router = APIRouter()
api_router.inlcude_router(login.router, tags=['login'])
api_router.include_router(article.router, prefix='/articles', tags=['articles'])
