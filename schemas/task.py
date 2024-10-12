from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True