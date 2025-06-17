# import_data.py

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Base, Equipment, Software, Accessory, Location, People, Inventory, Alias
)

# Connexion à la base SQLite
engine = create_engine('sqlite:///lab.db')
Session = sessionmaker(bind=engine)
session = Session()

def load_json(filename):
    with open(f"bdd/{filename}", encoding='utf-8') as f:
        return json.load(f)

# 1. Software
for data in load_json("software.json"):
    session.add(Software(**data))

# 2. Equipment
for data in load_json("equipment.json"):
    session.add(Equipment(**data))

# 3. Accessories
for data in load_json("accessories.json"):
    session.add(Accessory(**data))

# 4. Locations
for data in load_json("locations.json"):
    session.add(Location(**data))

# 5. People (avec relations spécialisations + lieux)
people_data = load_json("people.json")
for data in people_data:
    specializations = data.pop("specializations", [])
    locations = data.pop("locations", [])
    person = People(**data)
    for spec_id in specializations:
        equipment = session.get(Equipment, spec_id)
        if equipment:
            person.specializations.append(equipment)
    for loc_id in locations:
        location = session.get(Location, loc_id)
        if location:
            person.locations.append(location)
    session.add(person)

# 6. Inventory
inventory_data = load_json("inventory.json")
for data in inventory_data:
    session.add(Inventory(**data))

# 7. Aliases
alias_data = load_json("aliases.json")
for data in alias_data:
    session.add(Alias(**data))

# Commit final
session.commit()
print("✅ Données importées avec succès depuis les fichiers JSON.")
