from app.database import SessionLocal
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService
from app.models.user import RoleEnum

def test_register():
    db = SessionLocal()
    try:
        user_in = UserCreate(
            email="debug@test.com",
            password="password123",
            full_name="Debug User",
            role=RoleEnum.student
        )
        svc = UserService(db)
        user = svc.register_user(user_in)
        print("Success:", user.email)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_register()
