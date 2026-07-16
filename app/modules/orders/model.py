from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Client(Base):
    __tablename__ = "clienti"
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(100), nullable=False)
    telefon = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    comenzi = relationship("Comanda", back_populates="client")

class Comanda(Base):
    __tablename__ = "comenzi"
    id_comanda = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(Integer, ForeignKey("clienti.id_client"), nullable=False)
    data_comanda = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), default=0.00, nullable=False)

    client = relationship("Client", back_populates="comenzi")
    lumanari = relationship("ComandaLumanare", back_populates="comanda", cascade="all, delete-orphan")

class ComandaLumanare(Base):
    __tablename__ = "comenzi_lumanari"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_comanda = Column(Integer, ForeignKey("comenzi.id_comanda", ondelete="CASCADE"), nullable=False)
    id_lumanare = Column(Integer, ForeignKey("lumanari.id_lumanare"), nullable=False)
    cantitate = Column(Integer, nullable=False)
    pret_unitar = Column(Numeric(10, 2), nullable=False)

    comanda = relationship("Comanda", back_populates="lumanari")
    lumanare = relationship("Lumanare", back_populates="comenzi_asociate")
