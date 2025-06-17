# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# === TABLES ASSOCIATIVES ===

# People <-> Equipment (specializations)
people_equipment = Table(
    'people_equipment',
    Base.metadata,
    Column('person_id', ForeignKey('people.id'), primary_key=True),
    Column('equipment_id', ForeignKey('equipment.id'), primary_key=True)
)

# People <-> Location (frequent presence)
people_location = Table(
    'people_location',
    Base.metadata,
    Column('person_id', ForeignKey('people.id'), primary_key=True),
    Column('location_id', ForeignKey('locations.id'), primary_key=True)
)

# Equipment <-> Software (tools used with equipment)
equipment_software = Table(
    'equipment_software',
    Base.metadata,
    Column('equipment_id', ForeignKey('equipment.id'), primary_key=True),
    Column('software_id', ForeignKey('software.id'), primary_key=True)
)

# === TABLES PRINCIPALES ===

class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    role = Column(String)

    # Relations
    specializations = relationship('Equipment', secondary=people_equipment, back_populates='specialists')
    locations = relationship('Location', secondary=people_location, back_populates='people')


class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    category = Column(String)
    description = Column(Text)

    # Relations
    specialists = relationship('People', secondary=people_equipment, back_populates='specializations')
    inventories = relationship('Inventory', back_populates='equipment')
    software = relationship('Software', secondary=equipment_software, back_populates='equipment')


class Software(Base):
    __tablename__ = 'software'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)

    # Relations
    equipment = relationship('Equipment', secondary=equipment_software, back_populates='software')


class Accessory(Base):
    __tablename__ = 'accessories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    description = Column(Text)

    # Relations
    inventories = relationship('Inventory', back_populates='accessory')


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)

    # Relations
    inventories = relationship('Inventory', back_populates='location')
    people = relationship('People', secondary=people_location, back_populates='locations')


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=True)
    accessory_id = Column(Integer, ForeignKey('accessories.id'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'))

    # Relations
    equipment = relationship('Equipment', back_populates='inventories')
    accessory = relationship('Accessory', back_populates='inventories')
    location = relationship('Location', back_populates='inventories')


class Alias(Base):
    __tablename__ = 'aliases'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)               # nom alternatif, ex: "Oculus"
    target_type = Column(String, nullable=False)        # "equipment", "accessory", "software"
    target_id = Column(Integer, nullable=False)         # id réel dans la bonne table
