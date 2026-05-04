import os
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, or_, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker


class Base(DeclarativeBase):
    pass


class LoginCredential(Base):
    __tablename__ = "login_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    terms_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __getitem__(self, key):
        return getattr(self, key)


engine = None
SessionLocal = scoped_session(sessionmaker())


def get_db():
    return SessionLocal()


def close_db(error=None):
    SessionLocal.remove()


def init_db(app):
    global engine

    os.makedirs(app.instance_path, exist_ok=True)
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if database_url is None:
        database_path = app.config["DATABASE"]
        database_url = f"sqlite:///{database_path}"

    engine = create_engine(database_url)
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(engine)
    app.teardown_appcontext(close_db)


def save_login_credentials(username, password_hash):
    db = get_db()
    credential = LoginCredential(
        username=username,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc),
    )
    db.add(credential)
    db.commit()


def find_registered_user_by_identifier(identifier):
    db = get_db()
    return db.execute(
        select(RegisteredUser)
        .where(or_(RegisteredUser.username == identifier, RegisteredUser.email == identifier))
        .order_by(RegisteredUser.id.desc())
        .limit(1)
    ).scalar_one_or_none()


def save_registered_user(first_name, last_name, email, username, password_hash, terms_read):
    db = get_db()
    user = RegisteredUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password_hash=password_hash,
        terms_read=terms_read == "yes",
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
