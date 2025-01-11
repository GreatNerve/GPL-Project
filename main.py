from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware import Middleware
from config.dbConfig import init_db
from route.UserRoute import router as user_router
from middleware.HandleExceptions import HandleExceptionsMiddleware
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import disconnect
import uvicorn

@asynccontextmanager
async def lifespan_context(app_instance: FastAPI):
    print("Application starting up. Initializing...")
    init_db()
    yield
    # Add any cleanup code here if needed
    await on_cleanup()

async def on_cleanup():
    print("Application shutting down. Cleaning up...")
    disconnect()

middleware = [
    Middleware(HandleExceptionsMiddleware)
]

app = FastAPI(
    title="GPL API",
    version="0.1.0",
    lifespan=lifespan_context, middleware=middleware)

app.include_router(user_router, prefix="/api/v1/user", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)