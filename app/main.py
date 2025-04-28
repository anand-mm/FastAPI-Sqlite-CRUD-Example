from fastapi import  Depends, FastAPI
from app.db import create_table
from app.items import items
from app.auth import auth_routes
from app.auth.auth import restrict_users_for, verify_token
from app.users import users

app = FastAPI()

create_table()

common_dependency = [Depends(verify_token), Depends(restrict_users_for)]
# app.include_router(master.router,dependencies=[Depends(verify_token)])

app.include_router(auth_routes.router)
    
app.include_router(items.router,dependencies=common_dependency)

app.include_router(users.router,dependencies=common_dependency)
