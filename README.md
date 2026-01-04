## Setup Instructions

- Install SQL Server (Express / Developer)
- Create a database
- Install ODBC Driver 17 for SQL Server
- Clone repo
- Copy `.env.example` → `.env`
- Update DB credentials
- Install dependencies:
  pip install -r requirements.txt
-
- Run server:
  `uvicorn app.main:app --reload` or `python -m uvicorn app.main:app --reload`
