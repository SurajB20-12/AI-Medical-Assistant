from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exceptions_middleware
app = FastAPI(title="Medical AI Assistant", description="An AI assistant for medical queries.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#middleware exception handling
app.middleware("http")(catch_exceptions_middleware)


