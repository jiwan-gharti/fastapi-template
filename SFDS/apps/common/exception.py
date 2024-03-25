from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from main import app


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     if exc.status_code == status.HTTP_401_UNAUTHORIZED:
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={"detail": "Unauthorized"},
#         )
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail},
#     )