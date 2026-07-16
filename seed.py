from datetime import date
from decimal import Decimal
from app.db.connection import SessionLocal, engine, Base
from app.core.base import Ceara, Sezon, Forma, Parfum, Culoare, Lumanare, Client, Comanda, ComandaLumanare, Material, Productie, ConsumMateriale

def populate_database():
    print("Curatare tabele vechi din Neon Cloud...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creare structura noua si curata...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Inserare nomenclatoare...")
        ceara_nat = Ceara(nume_ceara="Ceara naturala")
        parafina = Ceara(nume_ceara="Parafina")
        db.add_all([ceara_nat, parafina])
        
        sezoane_list = [Sezon(nume_sezon=n) for n in ['Craciun', 'Revelion', 'Ziua indragostitilor', 'Paste', 'Botez', 'Nunta', 'Onomastica', 'Zi de nastere', 'Tema religioasa', 'Piese sah', 'Relax']]
        db.add_all(sezoane_list)
        
        forme_list = [Forma(nume_forma=n) for n in ['Brad', 'Bradut', 'Stea', 'Clopotel', 'Glob-uter matern', 'Cadou ambalat', 'Fulg de nea', 'Con de brad', 'Calice mare', 'Calice mic', 'Lacramioare incorporate L', 'Lacramioare incorporate M', 'Cuplu imbratisat', 'Inimioare in cub', 'Inima radianta', 'Inima afectiva', 'Inimioara diamant', 'Uniti pentru totdeauna', 'Sfanta familie', 'Acoperamantul Maicii Domnului', 'Luna', 'Pamant', 'Astronaut', 'Lalea', 'Buchet mireasa S', 'Buchet mireasa M', 'Buchet mireasa l', 'Buchet mireasa XL', 'Ou floral XXL', 'Ou floral L', 'Ou de Paste', 'Diamnat', 'Cub segmentat', 'Cub de bile', 'Quadrifoglio L', 'Quadrifoglio S', 'Zimtat L', 'Zimtat M', 'Amintiri', 'Obiective interioare', 'Obiective exterioare', 'Hexagon', 'Patrat radiant', 'Labuta catel', 'Bufnita', 'Patrat fin', 'Oval fin', 'Rotund fin', 'Inima fina']]
        db.add_all(forme_list)
        
        parfumuri_list = [Parfum(nume_parfum=n) for n in ['Sandal', 'Ylang Ylang', 'Portocala', 'Lamaie', 'Frezie', 'Lavanda', 'Menta', 'Iasomie', 'Flori de cires']]
        db.add_all(parfumuri_list)
        
        culori_list = [Culoare(nume_culoare=n) for n in ['Natural ceara', 'Alb-cristal', 'Rosu', 'Albastru', 'Verde', 'Galben']]
        db.add_all(culori_list)
        db.commit()
        
        print("Inserare produse de catalog...")
        brad_premium = Lumanare(nume="Brad Craciun Premium", id_ceara=1, id_sezon=1, id_forma=1, id_parfum=1, id_culoare=2, pret=Decimal("35.00"), stoc=20)
        ou_elegant = Lumanare(nume="Ou Paste Elegant", id_ceara=2, id_sezon=4, id_forma=31, id_parfum=2, id_culoare=3, pret=Decimal("25.00"), stoc=15)
        db.add_all([brad_premium, ou_elegant])
        db.commit()
        
        print("Inserare clienti si comenzi...")
        maria = Client(nume="Maria Pop", telefon="0711111111", email="maria@gmail.com")
        ion = Client(nume="Ion Ionescu", telefon="0722222222", email="ion@gmail.com")
        db.add_all([maria, ion])
        db.commit()
        
        comanda_1 = Comanda(id_client=1, data_comanda=date(2026, 12, 1), total=Decimal("120.00"))
        comanda_2 = Comanda(id_client=2, data_comanda=date(2026, 12, 5), total=Decimal("80.00"))
        db.add_all([comanda_1, comanda_2])
        db.commit()
        
        pivot_1 = ComandaLumanare(id_comanda=1, id_lumanare=1, cantitate=2, pret_unitar=Decimal("35.00"))
        pivot_2 = ComandaLumanare(id_comanda=1, id_lumanare=2, cantitate=1, pret_unitar=Decimal("25.00"))
        db.add_all([pivot_1, pivot_2])
        
        print("Inserare materiale de productie...")
        mat_ceara = Material(nume_material="Ceara naturala", unitate="kg")
        mat_fitil = Material(nume_material="Fitil", unitate="buc")
        mat_colorant = Material(nume_material="Colorant rosu", unitate="ml")
        db.add_all([mat_ceara, mat_fitil, mat_colorant])
        db.commit()
        
        prod_1 = Productie(id_lumanare=1, data_productie=date(2026, 11, 20), cantitate=50)
        prod_2 = Productie(id_lumanare=2, data_productie=date(2026, 3, 15), cantitate=30)
        db.add_all([prod_1, prod_2])
        db.commit()
        
        consum_1 = ConsumMateriale(id_productie=1, id_material=1, cantitate_consumata=Decimal("5.50"))
        consum_2 = ConsumMateriale(id_productie=1, id_material=2, cantitate_consumata=Decimal("50.00"))
        consum_3 = ConsumMateriale(id_productie=1, id_material=3, cantitate_consumata=Decimal("20.00"))
        db.add_all([consum_1, consum_2, consum_3])
        
        db.commit()
        print("Succes! Toate datele reale ale magazinului au fost incarcate sincron.")
    except Exception as e:
        db.rollback()
        print(f"Eroare la inserarea datelor: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()