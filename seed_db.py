from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base
import bcrypt

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def create_demo_user():
    db = SessionLocal()
    try:
        username = "demo"
        password = "123"
        
        # Check if exists
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"User '{username}' already exists.")
            return

        # Create user
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password_hash=hashed)
        
        db.add(new_user)
        db.commit()
        print(f"User '{username}' created successfully with password '{password}'.")
        
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
