from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    # Relationship to batteries.
    batteries = relationship("Battery", back_populates="location", cascade="all, delete-orphan")

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String)
    # Relationships to battery_company and tariffs.
    battery_companies = relationship("BatteryCompany", back_populates="company", cascade="all, delete-orphan")
    tariffs = relationship("Tariff", back_populates="company", cascade="all, delete-orphan")

class Battery(Base):
    __tablename__ = "batteries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    current_charge = Column(Float, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    last_maintenance = Column(Date)
    # Relationships to location, battery_company, telemetry, and tariffs.
    location = relationship("Location", back_populates="batteries")
    battery_companies = relationship("BatteryCompany", back_populates="battery", cascade="all, delete-orphan")
    telemetry_records = relationship("Telemetry", back_populates="battery", cascade="all, delete-orphan")
    tariffs = relationship("Tariff", back_populates="battery", cascade="all, delete-orphan")

class BatteryCompany(Base):
    __tablename__ = "battery_company"
    battery_id = Column(Integer, ForeignKey("batteries.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)
    role = Column(String, primary_key=True)
    # Relationships to battery and company.
    battery = relationship("Battery", back_populates="battery_companies")
    company = relationship("Company", back_populates="battery_companies")

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"))
    timestamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    energy_in = Column(Float)
    energy_out = Column(Float)
    # Relationship to battery.
    battery = relationship("Battery", back_populates="telemetry_records")

class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    battery_id = Column(Integer, ForeignKey("batteries.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    rate = Column(Float)
    description = Column(String)
    effective_date = Column(Date)
    # Relationships to battery and company.
    battery = relationship("Battery", back_populates="tariffs")
    company = relationship("Company", back_populates="tariffs") 