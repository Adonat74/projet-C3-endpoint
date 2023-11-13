from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# CREATING MODELS FOR THE POSTGRES TABLES


class Chiffre(Base):
    __tablename__ = "chiffres_affaire"

    id = Column(Integer, primary_key=True, nullable=False)
    chiffre_affaire = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    salon_name = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
    region = Column(String, nullable=False)
    department = Column(String, nullable=False)
    open_date = Column(Date, nullable=False)
    number_employees = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
