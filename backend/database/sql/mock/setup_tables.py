from sqlalchemy import text
from backend.database.sql.database import get_engine

def create_tables():
    engine = get_engine("default")
    with engine.begin() as connection:
        # Create locations table.
        create_locations = """
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            country TEXT
        );
        """
        connection.execute(text(create_locations))
        print("Created table: locations")

        # Create companies table.
        create_companies = """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT
        );
        """
        connection.execute(text(create_companies))
        print("Created table: companies")

        # Create batteries table.
        create_batteries = """
        CREATE TABLE IF NOT EXISTS batteries (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            capacity REAL NOT NULL,
            current_charge REAL NOT NULL,
            location_id INTEGER,
            last_maintenance DATE,
            FOREIGN KEY(location_id) REFERENCES locations(id)
        );
        """
        connection.execute(text(create_batteries))
        print("Created table: batteries")

        # Create battery_company join table.
        create_battery_company = """
        CREATE TABLE IF NOT EXISTS battery_company (
            battery_id INTEGER,
            company_id INTEGER,
            role TEXT,
            PRIMARY KEY (battery_id, company_id, role),
            FOREIGN KEY (battery_id) REFERENCES batteries(id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        );
        """
        connection.execute(text(create_battery_company))
        print("Created table: battery_company")

        # Create telemetry table.
        create_telemetry = """
        CREATE TABLE IF NOT EXISTS telemetry (
            id SERIAL PRIMARY KEY,
            battery_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            energy_in REAL,
            energy_out REAL,
            FOREIGN KEY (battery_id) REFERENCES batteries(id)
        );
        """
        connection.execute(text(create_telemetry))
        print("Created table: telemetry")

        # Create tariffs table.
        create_tariffs = """
        CREATE TABLE IF NOT EXISTS tariffs (
            id SERIAL PRIMARY KEY,
            battery_id INTEGER,
            company_id INTEGER,
            rate REAL,
            description TEXT,
            effective_date DATE,
            FOREIGN KEY (battery_id) REFERENCES batteries(id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        );
        """
        connection.execute(text(create_tariffs))
        print("Created table: tariffs")

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.") 