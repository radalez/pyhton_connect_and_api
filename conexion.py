from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import SQLAlchemyError
import logging

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    publicaciones = relationship("Publicaciones", back_populates="user", cascade="all, delete-orphan")


class Publicaciones(Base):
    __tablename__ = "publicaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)

    user_id = Column(ForeignKey("usuarios.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="publicaciones")

engine = create_engine(
    "sqlite:///database.db",
    connect_args={"check_same_thread": True},
    echo = True
)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class UserAdmin:
    def __init__(self):
        self.session = Session()

    def add_user(self, name, email):
        try:
            user = User(name=name, email=email)
            self.session.add(user)
            self.session.commit()
            logging.info("Usuario agregado correctamente")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error: {e}")
            logging.error(f"No se pudo agregar usuario. ERROR: {e}")
            raise e

    def update_user(self, email, name):
        try:
            if not name or not email:
                raise ValueError("El nombre y el correo no pueden estar vacíos.")
            user = self.session.query(User).filter_by(email = email).first()
            if user:
                user.name = name
                self.session.commit()
            else:
                logging.warning(f"Usuario con el email: {email} no localizado")

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error al actualizar: {e} ")
            logging.error(f"No se pudo actualizar usuario.ERROR: {e}")
            raise e

    def delete_user(self, email):
        try:
            user = self.session.query(User).filter_by(email=email).first()
            if user:
                self.session.delete(user)
                self.session.commit()
            else:
                logging.warning(f"Usuario con el email: {email} no localizado")

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error al eliminar usuario: {e} ")
            logging.error(f"No se pudo eliminar usuario. ERROR: {e}")
            raise e

    def get_users(self):
        try:
            users = self.session.query(User).all()
            return users
        except SQLAlchemyError as e:
            print(f"Error al conseguir usuarios: {e} ")
            logging.error(f"No se pudo conseguir usuarios. ERROR: {e}")
            raise e

    def delete_all_users(self):
        try:
            users = self.session.query(User).delete()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error al eliminar usuarios: {e} ")
            logging.error(f"No se pudo eliminar usuarios. ERROR: {e}")
            raise e




