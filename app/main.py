from fastapi import  Depends, FastAPI
from app.db import create_table
from app.routes import master,auth_routes, users
from app.security.auth import restrict_users_for, verify_token

app = FastAPI()

create_table()

common_dependency = [Depends(verify_token), Depends(restrict_users_for)]
# app.include_router(master.router,dependencies=[Depends(verify_token)])

app.include_router(auth_routes.router)
    
app.include_router(master.router,dependencies=common_dependency)

app.include_router(users.router,dependencies=common_dependency)
