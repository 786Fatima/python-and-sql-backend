## Setup Instructions

1. Install SQL Server (Express / Developer)
2. Create a database
3. Install ODBC Driver 17 for SQL Server
4. Clone repo
5. Copy `.env.example` → `.env`
6. Update DB credentials
7. Install dependencies:
   pip install -r requirements.txt
8. Run server:
   `uvicorn app.main:app --reload` or `python -m uvicorn app.main:app --reload`
