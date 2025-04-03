from fastapi import  Depends, FastAPI
from app.db import create_table
from app.routes import master,auth_routes
from app.security.auth import verify_token

app = FastAPI()

create_table()

# app.include_router(master.router,dependencies=[Depends(verify_token)])

app.include_router(auth_routes.router)
    
app.include_router(master.router)
