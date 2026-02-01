from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import Users
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = Users(
        email = user.email,
        password = Hasher.get_password_hash(user.password),
        is_active = True,
        is_superuser = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
