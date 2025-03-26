from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base): # Пользователи
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String)


class Event(Base): # Мероприятия
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger) # telegram id
    title_event: Mapped[str] = mapped_column(String) # название мероприятия


class Tasks(Base): # Задачи
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    title_task: Mapped[str] = mapped_column(String) # Название задачи
    id_event: Mapped[int] = mapped_column(Integer) # id мероприятия из таблицы Event
    deadline_task: Mapped[str] = mapped_column(String, default='note') # срок дедлайна
    status_task: Mapped[str] = mapped_column(String, default='active') # статус задачи


class Expenses(Base): # Расходы
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    title_expense: Mapped[str] = mapped_column(String) # категория расхода
    amount_expense: Mapped[str] = mapped_column(String, default='note') # сумма расхода
    id_event: Mapped[int] = mapped_column(Integer) # id мероприятия из таблицы Event
    date_expense: Mapped[str] = mapped_column(String) # id расхода


class CurrentEvent(Base): # мероприятие, которое выбрал исполнитель
    __tablename__ = 'current_event'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_event: Mapped[int] = mapped_column(BigInteger) # id мероприятия из таблицы Event
    tg_id: Mapped[int] = mapped_column(BigInteger)
    title_event: Mapped[str] = mapped_column(String)  # название мероприятия


class Performers(Base): # Исполнители
    __tablename__ = 'performers'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name_performer: Mapped[str] = mapped_column(String) # Имя исполнителя
    category_performer: Mapped[str] = mapped_column(String) # категория исполнителя
    photo_performer: Mapped[str] = mapped_column(String) # фото исполнителя
    reiting_performer: Mapped[str] = mapped_column(String, default='не указано') # рейтинг исполнителя
    cost_performer: Mapped[str] = mapped_column(String, default='не указано')# стоимость исполнителя
    phone_performer: Mapped[str] = mapped_column(String, default='не указано') # телефон исполнителя
    profile_performer: Mapped[str] = mapped_column(String, default='не указано') # ссылка на профиль исполнителя
    description_performer: Mapped[str] = mapped_column(String, default='не указано') # описание исполнителя


class Locations(Base): # Локации
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name_location: Mapped[str] = mapped_column(String) # наименование локации
    category_location: Mapped[int] = mapped_column(BigInteger) # категория локации
    description_location: Mapped[str] = mapped_column(String, default='не указано') # описание локации
    photo_location: Mapped[str] = mapped_column(String) # фото локации
    adress_location: Mapped[str] = mapped_column(String, default='не указано') # адрес локации
    area_location: Mapped[str] = mapped_column(String, default='не указано') # площадь локации
    capacity_location: Mapped[str] = mapped_column(String, default='не указано') # вместимость локации
    reiting_location: Mapped[str] = mapped_column(String, default='не указано') # рейтинг локации
    cost_location: Mapped[str] = mapped_column(String, default='не указано') # стоимость локации
    phone_location: Mapped[str] = mapped_column(String, default='не указано') # телефон локации
    profile_location: Mapped[str] = mapped_column(String, default='не указано') # профиль локации
    additional_photo_location: Mapped[str] = mapped_column(String, default='') # дополнительные фотографии локации


class Feedback(Base): # Отзывы об исполнителях
    __tablename__ = 'feedback'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    id_performer: Mapped[int] = mapped_column(BigInteger)  # id исполнителя из таблицы Performers
    feedback: Mapped[str] = mapped_column(String)  # текст отзыва об исполнителе


class EventFeedback(Base): # Отзывы о мероприятиях
    __tablename__ = 'event_feedback'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    id_event: Mapped[int] = mapped_column(BigInteger) # id мероприятия из таблицы Event
    estimation: Mapped[int] = mapped_column(Integer, default=0) # оценка мероприятия
    feedback: Mapped[str] = mapped_column(String) # отзыв о мероприятии


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)