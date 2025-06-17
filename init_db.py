from sqlalchemy import create_engine
from models import Base

# Création du moteur de base SQLite, qui va créer un fichier lab.db
engine = create_engine('sqlite:///lab.db', echo=True)

# Création de toutes les tables à partir des définitions dans models.py
Base.metadata.create_all(engine)

print("Base de données créée avec succès (structure uniquement).")
