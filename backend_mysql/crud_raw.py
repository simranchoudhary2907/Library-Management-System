from .db import get_conn
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user:
        return None
    if not pwd.verify(password, user['hashed_password']):
        return None
    return user

def list_books():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, title, author, category, available FROM books ORDER BY title LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_stats():
    # Example aggregated stats
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DATE_FORMAT(issue_date, '%Y-%m-01') AS month, COUNT(*) AS issued FROM borrow_records GROUP BY month ORDER BY month")
    series = cur.fetchall()
    cur.execute("SELECT category AS name, COUNT(*) AS value FROM books GROUP BY category")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return {'series': series, 'categories': categories}
