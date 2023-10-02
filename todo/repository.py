import hashlib
import os

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html

from .db import Task, User, engine
from sqlalchemy import insert, select, update, delete  # type: ignore
from sqlalchemy.orm import Session

def add_user(username: str, password: str) -> int:
  """Добавляет в таблицу user пользователя.
  
  Args:
    username: Имя пользователя.
    password: Пароль пользователя. 
    
  Returns:
    ID нового пользователя(User.id)"""
  with Session(engine) as session:
    stmt = insert(User) \
      .values(username = username, hashed_password = hash_password(password)) \
      .returning(User.id)
    result = session.execute(stmt).fetchone()
    session.commit()
  return result

# https://docs.sqlalchemy.org/en/20/tutorial/data_select.html

def get_user(username: str) -> User | None:
  """Возвращает пользователя с заданным именем."""
  with Session(engine) as session:
    stmt = select(User).where(User.username == username)
    result = session.scalars(stmt).first()
  return result

def get_all_task(id_user: int) -> list[Task]:
  """Возвращает все задачи, конкретного пользователя.

  Args:
    id_user: ID пользователя, задачи которого нужно вернуть.

  Returns:
    Список задач, созданных данным пользователем."""
  with Session(engine) as session:
    stmt = select(Task).where(Task.id_user == id_user)
    result = list(session.scalars(stmt).all())
  return result


def add_task(task: str, description: str, id_user: int, done: bool) -> int:
  """Добавляет в таблицу task описание нового слова.
  
  Args:
    task: Задача.
    description: Описание задачи.
    id_user: ID пользователя.
    done: Логичегое значение выполнена задача или нет

  Returns:
    ID новой задачи (Task.id).
  """

  with Session(engine) as session:
    stmt = insert(Task) \
      .values(name=task, description=description, id_user=id_user, done=done) \
      .returning(Task.id)

    result = session.scalars(stmt).first()
    session.commit()
  return result  # type: ignore

# https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-core-update-delete

def user_exists(username: str) -> bool:
  """Проверяет, существует ли пользователь с заданным именем."""
  return get_user(username) is not None

# stmt = (
# ...     update(user_table)
# ...     .where(user_table.c.name == "patrick")
# ...     .values(fullname="Patrick the Star")
# ... )
def mark_task_done(id: int):
  """Изменяет, статут задачи (волнена или нет)"""
  with Session(engine) as session:
    stmt = update(Task) \
      .where(Task.id == id) \
      .values(done = True)
    session.execute(stmt)
    session.commit()

def delet_task(id: int):
  """Удаляет, задачу"""
  with Session(engine) as session:
    stmt = delete(Task) \
      .where(Task.id == id) 
    session.execute(stmt)
    session.commit()

def hash_password(password: str) -> str:
  """Зашифровывает пароль.

    Для одного и того же пароля, функция ВСЕГДА выдает один и тот же результат.
    Это нужно для того, чтобы при авторизации можно было сравнить введенный пароль
    с зашифрованной версией, хранящейся в базе данных.
    
    Args:
      password: Незашифрованный пароль.
      
    Returns:
      Зашифрованная версия пароля."""

  return hashlib.sha256(password.encode('utf-8')).hexdigest()
