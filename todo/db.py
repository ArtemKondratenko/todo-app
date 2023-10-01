from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column

db_filename = 'db.sqlite'

engine = create_engine(f"sqlite+pysqlite:///{db_filename}")


def create_tables():
  """Создает в самой базе данных таблицы, на основе классов, наследуемых от Base"""
  Base.metadata.create_all(engine)


class Base(MappedAsDataclass, DeclarativeBase):
  """Базовый класс (т.е. класс, используемый в качестве родительского) для классов,
    которые представляют таблицы в базе данных."""
  pass


class User(Base):
  """Класс, представляющий пользователя нашего приложения."""

  __tablename__ = "user"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  username: Mapped[str]
  hashed_password: Mapped[str]


class Task(Base):
  """Задача конкретного пользователя."""

  __tablename__ = "task"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  id_user: Mapped[int]
  name: Mapped[str]
  description: Mapped[str]
  done: Mapped[bool]


