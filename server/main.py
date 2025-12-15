from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exceptions_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

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

app.include_router(upload_router)

app.include_router(ask_router)

