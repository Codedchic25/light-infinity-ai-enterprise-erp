from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Material(Base):
    __tablename__ = "materiale"
    id_material = Column(Integer, primary_key=True, autoincrement=True)
    nume_material = Column(String(100), nullable=False, unique=True)
    unitate = Column(String(20), nullable=False)
    consumuri = relationship("ConsumMateriale", back_populates="material")

class Productie(Base):
    __tablename__ = "productie"
    id_productie = Column(Integer, primary_key=True, autoincrement=True)
    id_lumanare = Column(Integer, ForeignKey("lumanari.id_lumanare"), nullable=False)
    data_productie = Column(Date, nullable=False)
    cantitate = Column(Integer, nullable=False)

    lumanare = relationship("Lumanare", back_populates="productii")
    materiale_consumate = relationship("ConsumMateriale", back_populates="productie", cascade="all, delete-orphan")

class ConsumMateriale(Base):
    __tablename__ = "consum_materiale"
    id_consum = Column(Integer, primary_key=True, autoincrement=True)
    id_productie = Column(Integer, ForeignKey("productie.id_productie", ondelete="CASCADE"), nullable=False)
    id_material = Column(Integer, ForeignKey("materiale.id_material"), nullable=False)
    cantitate_consumata = Column(Numeric(10, 2), nullable=False)

    productie = relationship("Productie", back_populates="materiale_consumate")
    material = relationship("Material", back_populates="consumuri")
