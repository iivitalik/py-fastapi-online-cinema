from app.database import SessionLocal
from app.models import UserGroup, UserGroupEnum

def seed_data():
    db = SessionLocal()
    try:
        for group_name in UserGroupEnum:
            exists = db.query(UserGroup).filter(UserGroup.name == group_name).first()
            if not exists:
                db.add(UserGroup(name=group_name))
                print(f"Added group: {group_name}")
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
