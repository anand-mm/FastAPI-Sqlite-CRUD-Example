from fastapi import Request
from fastapi.responses import JSONResponse

from app.users.exception import CustomException


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"error": f"Oops! {exc.name} caused a custom error."},
    )