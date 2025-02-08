from fastapi import FastAPI
from database import engine, Base
from account.account_api import user_router
from admin.admin_api import admin_router
app = FastAPI(docs_url='/')
app.include_router(user_router, prefix='/user')
app.include_router(admin_router, prefix='/admin')
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)