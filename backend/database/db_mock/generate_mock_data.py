from sqlalchemy import text
from backend.database.database import get_engine

def insert_mock_data():
    engine = get_engine("default")
    with engine.begin() as connection:
        # Insert locations.
        locations = [
            {"name": "Site 1", "address": "123 Energy Blvd", "city": "Springfield", "state": "IL", "country": "USA"},
            {"name": "Site 2", "address": "456 Power St", "city": "Metropolis", "state": "NY", "country": "USA"}
        ]
        for loc in locations:
            insert_loc = text("INSERT INTO locations (name, address, city, state, country) VALUES (:name, :address, :city, :state, :country)")
            connection.execute(insert_loc, loc)
            print(f"Inserted location: {loc['name']}")

        # Insert companies.
        companies = [
            {"name": "Installer Inc", "type": "installer"},
            {"name": "Retailer LLC", "type": "retailer"}
        ]
        for comp in companies:
            insert_comp = text("INSERT INTO companies (name, type) VALUES (:name, :type)")
            connection.execute(insert_comp, comp)
            print(f"Inserted company: {comp['name']}")

        # Insert batteries (assuming location ids 1 and 2 from above).
        batteries = [
            {"name": "Battery Alpha", "capacity": 500.0, "current_charge": 450.0, "location_id": 1, "last_maintenance": "2023-09-01"},
            {"name": "Battery Beta", "capacity": 750.0, "current_charge": 300.0, "location_id": 2, "last_maintenance": "2023-08-15"},
            {"name": "Battery Gamma", "capacity": 600.0, "current_charge": 600.0, "location_id": 1, "last_maintenance": "2023-07-20"}
        ]
        for bat in batteries:
            insert_bat = text("INSERT INTO batteries (name, capacity, current_charge, location_id, last_maintenance) VALUES (:name, :capacity, :current_charge, :location_id, :last_maintenance)")
            connection.execute(insert_bat, bat)
            print(f"Inserted battery: {bat['name']}")

        # Insert battery_company relations.
        battery_companies = [
            {"battery_id": 1, "company_id": 1, "role": "installer"},
            {"battery_id": 1, "company_id": 2, "role": "retailer"},
            {"battery_id": 2, "company_id": 1, "role": "installer"},
            {"battery_id": 2, "company_id": 2, "role": "retailer"},
            {"battery_id": 3, "company_id": 1, "role": "installer"}
        ]
        for bc in battery_companies:
            insert_bc = text("INSERT INTO battery_company (battery_id, company_id, role) VALUES (:battery_id, :company_id, :role)")
            connection.execute(insert_bc, bc)
            print(f"Inserted battery_company: Battery {bc['battery_id']} - Company {bc['company_id']} as {bc['role']}")

        # Insert telemetry data.
        telemetry_data = [
            {"battery_id": 1, "timestamp": "2023-10-11 08:00:00", "energy_in": 50.5, "energy_out": 30.0},
            {"battery_id": 2, "timestamp": "2023-10-11 09:00:00", "energy_in": 60.0, "energy_out": 25.5},
            {"battery_id": 3, "timestamp": "2023-10-11 10:00:00", "energy_in": 40.0, "energy_out": 35.0}
        ]
        for tel in telemetry_data:
            insert_tel = text("INSERT INTO telemetry (battery_id, timestamp, energy_in, energy_out) VALUES (:battery_id, :timestamp, :energy_in, :energy_out)")
            connection.execute(insert_tel, tel)
            print(f"Inserted telemetry for battery: {tel['battery_id']}")

        # Insert tariffs.
        tariffs = [
            {"battery_id": 1, "company_id": 1, "rate": 0.10, "description": "Standard installer tariff", "effective_date": "2023-10-01"},
            {"battery_id": 2, "company_id": 2, "rate": 0.15, "description": "Standard retailer tariff", "effective_date": "2023-10-05"}
        ]
        for tar in tariffs:
            insert_tar = text("INSERT INTO tariffs (battery_id, company_id, rate, description, effective_date) VALUES (:battery_id, :company_id, :rate, :description, :effective_date)")
            connection.execute(insert_tar, tar)
            print(f"Inserted tariff for battery: {tar['battery_id']} with company: {tar['company_id']}")

if __name__ == "__main__":
    insert_mock_data()
    print("Mock data inserted successfully.") 