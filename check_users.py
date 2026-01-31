from database import SessionLocal
from models import User

def check_users():
    db = SessionLocal()
    users = db.query(User).all()
    print(f"Total Users: {len(users)}")
    for u in users:
        print(f"User: {u.username}, ID: {u.id}")
    db.close()

if __name__ == "__main__":
    check_users()
