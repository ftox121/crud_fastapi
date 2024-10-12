from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from api.endpoints import auth, tasks

from db import base
from db.session import engine
from schemas.task import TaskCreate

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(tasks.router)


@app.on_event("startup")
async def startup():
    base.Base.metadata.create_all(bind=engine)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."},
    )


@app.on_event("startup")
async def startup():
    base.Base.metadata.create_all(bind=engine)


@app.get("/tasks", dependencies=[Depends(limiter.limit("100/minute"))])
async def get_tasks():
    return {"tasks": "Here are your tasks"}


@app.post("/tasks", dependencies=[Depends(limiter.limit("100/minute"))])
async def create_task(task: TaskCreate):
    return {"task": "Created"}