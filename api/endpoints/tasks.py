from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.task import TaskCreate, TaskResponse
from crud import task_crud
from api.dependencies import get_db, get_current_active_user
from models.user import User

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return task_crud.create_task(db, task, owner_id=current_user.id)


@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return task_crud.get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    task = task_crud.get_task(db, task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_existing_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_task = task_crud.update_task(db, task_id=task_id, task=task, owner_id=current_user.id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_task = task_crud.delete_task(db, task_id=task_id, owner_id=current_user.id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}