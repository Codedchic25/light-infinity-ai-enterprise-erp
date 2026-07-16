from app.db.connection import Base

# Importam clasele exact asa cum au fost definite in modulele lor
from app.modules.products.model import Ceara, Sezon, Forma, Parfum, Culoare, Lumanare
from app.modules.orders.model import Client, Comanda, ComandaLumanare
from app.modules.production.model import Material, Productie, ConsumMateriale

# Metadata cumulat pentru motorul SQLAlchemy si Alembic
metadata = Base.metadata