# Instructions

- Install SQL Server (Express / Developer)

- Create a database

- Install ODBC Driver 17 for SQL Server

- Copy `.env.example` → `.env`

- Update DB credentials

- Install dependencies:
  `pip install -r requirements.txt`

- In case of any updates run:
  `python -m alembic revision --autogenerate -m "update comment"`, then
  `python -m alembic upgrade head`

- Run server:
  `uvicorn app.main:app --reload` or `python -m uvicorn app.main:app --reload`

- API docs in `http://127.0.0.1:8000/docs`
