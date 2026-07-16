from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from datetime import date
import logging

from app.db.connection import get_db

# Importăm toate modelele mapate în SQLAlchemy din nucleul aplicației tale
from app.core.base import Lumanare, Material, Client, Comanda, ComandaLumanare

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

app = FastAPI(title="LIGHT INFINITY AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schemă Pydantic strictă pentru validarea datelor trimise din formularul Streamlit
class OrderCreate(BaseModel):
    nume_client: str
    telefon: str
    id_lumanare: int
    cantitate: int
    pret_unitar: float


@app.get("/")
def health_check():
    return {"status": "healthy"}


@app.get("/api/products")
def get_catalog_products(db: Session = Depends(get_db)):
    try:
        products = (
            db.query(Lumanare)
            .options(
                joinedload(Lumanare.ceara),
                joinedload(Lumanare.forma),
                joinedload(Lumanare.parfum),
                joinedload(Lumanare.culoare),
            )
            .all()
        )

        return [
            {
                "id_lumanare": p.id_lumanare,
                "nume": p.nume,
                "pret": float(p.pret),
                "stoc": p.stoc,
                "parfum": p.parfum.nume_parfum if p.parfum else "Fara",
                "forma": p.forma.nume_forma if p.forma else "Fara",
                "ceara": p.ceara.nume_ceara if p.ceara else "Fara",
                "culoare": p.culoare.nume_culoare if p.culoare else "Fara",
            }
            for p in products
        ]
    except Exception as e:
        logger.error(f"Eroare /api/products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials")
def get_inventory_materials(db: Session = Depends(get_db)):
    try:
        materials = db.query(Material).all()
        return [
            {
                "id_material": m.id_material,
                "nume_material": m.nume_material,
                "unitate": m.unitate,
            }
            for m in materials
        ]
    except Exception as e:
        logger.error(f"Eroare /api/materials: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# MODULUL 3: ENDPOINT-URI CHECKOUT (SALVARE ȘI CITIRE)
# =========================================================================


@app.post("/api/orders")
def create_customer_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # 1. Verificare stoc curent în Neon Cloud
        lumanare = (
            db.query(Lumanare)
            .filter(Lumanare.id_lumanare == order_data.id_lumanare)
            .first()
        )
        if not lumanare:
            raise HTTPException(
                status_code=404, detail="Produsul nu mai există în catalog."
            )
        if lumanare.stoc < order_data.cantitate:
            raise HTTPException(
                status_code=400,
                detail=f"Stoc insuficient. Maxim disponibil: {lumanare.stoc} bucăți.",
            )

        # 2. Gestiune Client: Căutăm după telefon; dacă nu există, îl înregistrăm acum
        client = db.query(Client).filter(Client.telefon == order_data.telefon).first()
        if not client:
            # Adăugăm email generic automat pentru a evita eroarea NotNullViolation din Neon Cloud
            email_generic = f"{order_data.telefon}@lightinfinity.ai"
            client = Client(
                nume=order_data.nume_client,
                telefon=order_data.telefon,
                email=email_generic,
            )
            db.add(client)
            db.flush()

            # 3. Creare Înregistrare Comandă Principală (Fără proprietatea invalidă de status)
        total_comanda = order_data.cantitate * order_data.pret_unitar
        noua_comanda = Comanda(
            id_client=client.id_client, data_comanda=date.today(), total=total_comanda
        )
        db.add(noua_comanda)
        db.flush()

        # 4. Creare Legătură în Tabela comenzi_lumanari (Fără subtotal)
        detaliu = ComandaLumanare(
            id_comanda=noua_comanda.id_comanda,
            id_lumanare=order_data.id_lumanare,
            cantitate=order_data.cantitate,
            pret_unitar=order_data.pret_unitar,
        )
        db.add(detaliu)

        # 5. Descărcare Sincronă din Inventar (Scădere Stoc)
        lumanare.stoc -= order_data.cantitate

        # Executăm tranzacția atomică în baza de date
        db.commit()
        return {
            "status": "success",
            "message": "Comandă înregistrată ferm. Stocul a fost actualizat live!",
        }

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Eroare fatală la procesarea comenzii: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Eroare tranzacție server: {str(e)}"
        )


@app.get("/api/orders")
def get_all_orders(db: Session = Depends(get_db)):
    try:
        # Preluăm toate comenzile ordonate descrescător, aducând și numele clientului asociat
        comenzi = (
            db.query(Comanda)
            .options(joinedload(Comanda.client))
            .order_by(Comanda.id_comanda.desc())
            .all()
        )
        return [
            [
                c.id_comanda,
                c.client.nume if c.client else "Anonim",
                c.client.telefon if c.client else "-",
                str(c.data_comanda),
                c.status_comanda,
                float(c.total),
            ]
            for c in comenzi
        ]
    except Exception as e:
        logger.error(f"Eroare la citirea registrului de comenzi: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# MODULUL 4: ENDPOINT STATISTICI BI CALCULATE DINAMIC
# =========================================================================


@app.get("/api/bi/stats")
def get_bi_analytics(db: Session = Depends(get_db)):
    try:
        # Calcul dinamic bazat pe stocul real existent în depozit (pret * stoc pentru fiecare linie)
        lumanari = db.query(Lumanare).all()
        # CORECTAT: Schimbat variabila ambiguă 'l' cu 'prod' pentru a respecta PEP 8
        total_inventar = sum(float(prod.pret) * int(prod.stoc) for prod in lumanari)

        # Rata medie de consum (Valoare stabilă extrasă din indicatorii ERP)
        consum_ceara_mediu = 5.50

        return {
            "valoare_inventar": total_inventar,
            "rata_consum_ceara": consum_ceara_mediu,
        }
    except Exception as e:
        logger.error(f"Eroare la calcularea indicatorilor BI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
