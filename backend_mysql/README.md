Backend (MySQL + raw SQL) scaffold.

Setup:

1. Create a Python venv and install:

```bash
python -m venv .venv
. .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Configure environment in a `.env` file at the project root with:

```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASS=secret
DB_NAME=library_db
SECRET_KEY=change-me
```

3. Start the app:

```bash
uvicorn backend_mysql.main:app --reload --port 8000
```

Notes:
- This scaffold uses raw `mysql-connector-python` queries in `crud_raw.py`. Implement the `/api/token` endpoint and user management according to your auth requirements.
