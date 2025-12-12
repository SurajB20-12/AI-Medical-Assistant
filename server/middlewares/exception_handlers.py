from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception("Unhandled Exception")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )