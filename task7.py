# Создать RESTful API для управления списком задач. Приложение должно
# использовать FastAPI и поддерживать следующие функции:
# ○ Получение списка всех задач.
# ○ Получение информации о задаче по её ID.
# ○ Добавление новой задачи.
# ○ Обновление информации о задаче по её ID.
# ○ Удаление задачи по её ID.
# Каждая задача должна содержать следующие поля: ID (целое число),
# Название (строка), Описание (строка), Статус (строка): "todo", "in progress",
# "done".
import enum
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse

app = FastAPI()


class Status(enum.Enum):
    to_do = "to do"
    in_progress = "in progress"
    done = "done"


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Status

class NewTask(BaseModel):
    id: int
    title: str = Field()
    description: str = Field()
    status: Status


tasks = [
    Task(id=i, title=f'title_{i}', description=f'description_{i}', status=Status.to_do)
    for i in range(1, 6)
]

@app.get("/", response_model=list[Task])
@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_id(t_id: int = None):
    if not t_id:
        return tasks
    tasks_list = [t for t in tasks if t.id == t_id]
    return tasks_list


@app.post('/new_task')
async def create_task(task: NewTask):
    new_id = 1
    if tasks:
        new_id = max(tasks, key=lambda x: x.id).id + 1
    tasks.append(
        Task(
            id=new_id,
            title=task.title,
            description=task.description,
            status=Status.to_do
        )
    )
    return RedirectResponse(url="/users", status_code=303)


@app.put('/task_change', response_model=Task)
async def change_user(task: NewTask, task_id: int):
    upd_task = [t for t in tasks if t.id == task_id]
    if not upd_task:
        raise HTTPException(status_code=404, detail='Task not found')
    upd_task[0].title = task.title
    upd_task[0].description = task.description
    upd_task[0].status = task.status
    return upd_task


@app.delete('/task_delete', response_model=Task, summary="Delete task by id")
async def delete_task(task_id: int):
    del_task = [t for t in tasks if t.id == task_id]
    if not del_task:
        raise HTTPException(status_code=404, detail='Task not found')
    tasks.remove(del_task[0])
    return del_task[0]


if __name__ == '__main__':
    uvicorn.run(
        "task7:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )