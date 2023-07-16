# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


users = [
    User(id=1, name="Vasya", email="Vasya@mail.ru", password="asdfg"),
    User(id=1, name="Kolya", email="Kolya@mail.ru", password="12345")
]


@app.get('/', response_class=HTMLResponse)
@app.get('/users', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("item.html", {"request": request, "users": users})


@app.get('/new_user', response_class=HTMLResponse)
async def new_user(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request, "title": "Add User"})


@app.post("/add_user")
def add_user(user_name=Form(), user_email=Form(), user_password=Form()):
    new_id = 1
    if users:
        new_id = max(users, key=lambda x: x.id).id + 1
    users.append(
        User(
            id=new_id,
            name=user_name,
            email=user_email,
            password=user_password
        )
    )
    return RedirectResponse(url="/users", status_code=303)


if __name__ == '__main__':
    uvicorn.run(
        "task6:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )