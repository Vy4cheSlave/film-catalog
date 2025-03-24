# film-catalog

## REST API для управления библиотекой фильмов. Пользователь может добавлять фильмы, оставлять на них отзывы и выставлять рейтинг.

# Требования
- Python 3.x (3.13)
- FastAPI
- SQLAlchemy или другой ORM (SQLModel)
- SQLite или любая реляционная база данных (PostgreSQL)
- Pydantic для валидации данных
- Docker (docker-compose)

# Шаги запуска
1. Клонировать репозиторий:
```
git clone $(git remote get-url origin)
```
2. Перейти в корневую директорию проекта:
```
cd film-catalog
```
3. Запустить сервер:
```
docker-compose up
```

# URL
URL конечных путей - `http://localhost:8080/movies`.

# Swagger UI
Swagger URL - `http://localhost:8080/docs`.

