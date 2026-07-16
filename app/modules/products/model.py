from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Ceara(Base):
    __tablename__ = "ceara"
    id_ceara = Column(Integer, primary_key=True, autoincrement=True)
    nume_ceara = Column(String(100), nullable=False, unique=True)
    lumanari = relationship("Lumanare", back_populates="ceara")

class Sezon(Base):
    __tablename__ = "sezoane"
    id_sezon = Column(Integer, primary_key=True, autoincrement=True)
    nume_sezon = Column(String(100), nullable=False, unique=True)
    lumanari = relationship("Lumanare", back_populates="sezon")

class Forma(Base):
    __tablename__ = "forme"
    id_forma = Column(Integer, primary_key=True, autoincrement=True)
    nume_forma = Column(String(100), nullable=False, unique=True)
    lumanari = relationship("Lumanare", back_populates="forma")

class Parfum(Base):
    __tablename__ = "parfumuri"
    id_parfum = Column(Integer, primary_key=True, autoincrement=True)
    nume_parfum = Column(String(100), nullable=False, unique=True)
    lumanari = relationship("Lumanare", back_populates="parfum")

class Culoare(Base):
    __tablename__ = "culori"
    id_culoare = Column(Integer, primary_key=True, autoincrement=True)
    nume_culoare = Column(String(100), nullable=False, unique=True)
    lumanari = relationship("Lumanare", back_populates="culoare")

class Lumanare(Base):
    __tablename__ = "lumanari"
    id_lumanare = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(100), nullable=False)
    id_ceara = Column(Integer, ForeignKey("ceara.id_ceara"), nullable=False)
    id_sezon = Column(Integer, ForeignKey("sezoane.id_sezon"), nullable=False)
    id_forma = Column(Integer, ForeignKey("forme.id_forma"), nullable=False)
    id_parfum = Column(Integer, ForeignKey("parfumuri.id_parfum"), nullable=False)
    id_culoare = Column(Integer, ForeignKey("culori.id_culoare"), nullable=False)
    pret = Column(Numeric(10, 2), nullable=False)
    stoc = Column(Integer, default=0, nullable=False)

    ceara = relationship("Ceara", back_populates="lumanari")
    sezon = relationship("Sezon", back_populates="lumanari")
    forma = relationship("Forma", back_populates="lumanari")
    parfum = relationship("Parfum", back_populates="lumanari")
    culoare = relationship("Culoare", back_populates="lumanari")
    comenzi_asociate = relationship("ComandaLumanare", back_populates="lumanare")
    productii = relationship("Productie", back_populates="lumanare")
