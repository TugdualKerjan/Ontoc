import json
import sqlite3
from database import DATABASE_FILE, init_database

def seed_database():
    """Import data from data.json into the database."""
    print("Initializing database...")
    init_database()

    print("Loading data.json...")
    with open('data.json', 'r') as f:
        data = json.load(f)

    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA foreign_keys = ON")

    print("Clearing existing data...")
    conn.execute("DELETE FROM examples")
    conn.execute("DELETE FROM system_substrates")
    conn.execute("DELETE FROM substrates")
    conn.execute("DELETE FROM systems")

    print("Processing systems...")

    # Collect all unique substrates
    all_substrates = set()
    for system_data in data['data']:
        if 'substrate' in system_data:
            all_substrates.update(system_data['substrate'])

    # Insert substrates
    print(f"Inserting {len(all_substrates)} substrates...")
    for substrate in all_substrates:
        substrate_id = substrate.lower().replace(' ', '-')
        conn.execute("""
            INSERT OR IGNORE INTO substrates (id, name, description)
            VALUES (?, ?, ?)
        """, (substrate_id, substrate.title(), f"Systems using {substrate} substrates"))

    # Insert systems
    print(f"Processing {len(data['data'])} systems...")
    for system_data in data['data']:
        # Insert system
        conn.execute("""
            INSERT OR REPLACE INTO systems (
                id, name, realizes, description, determinism,
                reversibility, exactness, realization_type, computation_model
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            system_data['id'],
            system_data['name'],
            system_data.get('realizes'),
            system_data.get('description'),
            system_data.get('determinism'),
            system_data.get('reversibility'),
            system_data.get('exactness'),
            system_data.get('realization_type'),
            json.dumps(system_data.get('computation_model', []))
        ))

        # Insert system-substrate relationships
        if 'substrate' in system_data:
            for substrate in system_data['substrate']:
                substrate_id = substrate.lower().replace(' ', '-')
                conn.execute("""
                    INSERT OR IGNORE INTO system_substrates (system_id, substrate_id)
                    VALUES (?, ?)
                """, (system_data['id'], substrate_id))

        # Insert examples
        if 'examples' in system_data:
            for example in system_data['examples']:
                conn.execute("""
                    INSERT OR REPLACE INTO examples (
                        id, system_id, label, url, description, operations,
                        speed_category, scale_category, energy_per_operation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    example['id'],
                    system_data['id'],
                    example.get('label'),
                    example.get('url'),
                    example.get('description'),
                    json.dumps(example.get('operations', [])),
                    example.get('speed_category'),
                    example.get('scale_category'),
                    example.get('energy_per_operation')
                ))

    conn.commit()

    # Print stats
    system_count = conn.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
    substrate_count = conn.execute("SELECT COUNT(*) FROM substrates").fetchone()[0]
    example_count = conn.execute("SELECT COUNT(*) FROM examples").fetchone()[0]

    print(f"Database seeded successfully!")
    print(f"  Systems: {system_count}")
    print(f"  Substrates: {substrate_count}")
    print(f"  Examples: {example_count}")

    conn.close()

if __name__ == "__main__":
    seed_database()