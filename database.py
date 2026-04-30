import sqlite3
import json
import re
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

DATABASE_FILE = "ontoc.db"

def init_database():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA foreign_keys = ON")

    # Create tables
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS systems (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            realizes TEXT,
            description TEXT,
            determinism TEXT,
            reversibility TEXT,
            exactness TEXT,
            realization_type TEXT,
            computation_model TEXT
        );

        CREATE TABLE IF NOT EXISTS substrates (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS system_substrates (
            system_id TEXT REFERENCES systems(id),
            substrate_id TEXT REFERENCES substrates(id),
            PRIMARY KEY (system_id, substrate_id)
        );

        CREATE TABLE IF NOT EXISTS examples (
            id TEXT PRIMARY KEY,
            system_id TEXT REFERENCES systems(id),
            label TEXT,
            url TEXT,
            description TEXT,
            operations TEXT,
            speed_category TEXT,
            scale_category TEXT,
            energy_per_operation TEXT
        );
    """)

    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Get a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_system(system_id: str) -> Optional[Dict[str, Any]]:
    """Get a system by ID with its substrates and examples."""
    with get_db_connection() as conn:
        # Get system
        system = conn.execute(
            "SELECT * FROM systems WHERE id = ?", (system_id,)
        ).fetchone()

        if not system:
            return None

        system = dict(system)

        # Get substrates
        substrates = conn.execute("""
            SELECT s.* FROM substrates s
            JOIN system_substrates ss ON s.id = ss.substrate_id
            WHERE ss.system_id = ?
        """, (system_id,)).fetchall()
        system['substrates'] = [dict(row) for row in substrates]

        # Get examples
        examples = conn.execute(
            "SELECT * FROM examples WHERE system_id = ?", (system_id,)
        ).fetchall()
        system['examples'] = [dict(row) for row in examples]

        # Parse JSON fields
        if system['computation_model']:
            system['computation_model'] = json.loads(system['computation_model'])

        for example in system['examples']:
            if example['operations']:
                example['operations'] = json.loads(example['operations'])
            # Add thumbnail URL for YouTube videos
            if example['url']:
                example['thumbnail_url'] = get_youtube_thumbnail(example['url'])

        return system

def get_substrate(substrate_id: str) -> Optional[Dict[str, Any]]:
    """Get a substrate by ID."""
    with get_db_connection() as conn:
        substrate = conn.execute(
            "SELECT * FROM substrates WHERE id = ?", (substrate_id,)
        ).fetchone()
        return dict(substrate) if substrate else None

def get_systems_by_substrate(substrate_id: str) -> List[Dict[str, Any]]:
    """Get all systems that use a specific substrate."""
    with get_db_connection() as conn:
        systems = conn.execute("""
            SELECT s.* FROM systems s
            JOIN system_substrates ss ON s.id = ss.system_id
            WHERE ss.substrate_id = ?
            ORDER BY s.name
        """, (substrate_id,)).fetchall()

        result = []
        for system in systems:
            system_dict = dict(system)
            if system_dict['computation_model']:
                system_dict['computation_model'] = json.loads(system_dict['computation_model'])
            result.append(system_dict)

        return result

def get_all_systems() -> List[Dict[str, Any]]:
    """Get all systems."""
    with get_db_connection() as conn:
        systems = conn.execute("SELECT * FROM systems ORDER BY name").fetchall()
        result = []
        for system in systems:
            system_dict = dict(system)
            if system_dict['computation_model']:
                system_dict['computation_model'] = json.loads(system_dict['computation_model'])
            result.append(system_dict)
        return result

def get_all_substrates() -> List[Dict[str, Any]]:
    """Get all substrates."""
    with get_db_connection() as conn:
        substrates = conn.execute("SELECT * FROM substrates ORDER BY name").fetchall()
        return [dict(row) for row in substrates]

def get_systems_by_property(property_name: str, property_value: str) -> List[Dict[str, Any]]:
    """Get all systems that have a specific property value."""
    with get_db_connection() as conn:
        if property_name == "computation_model":
            # For JSON array fields, use JSON functions
            systems = conn.execute("""
                SELECT * FROM systems
                WHERE computation_model LIKE ?
                ORDER BY name
            """, (f'%"{property_value}"%',)).fetchall()
        else:
            # For regular string fields
            systems = conn.execute(f"""
                SELECT * FROM systems
                WHERE {property_name} = ?
                ORDER BY name
            """, (property_value,)).fetchall()

        result = []
        for system in systems:
            system_dict = dict(system)
            if system_dict['computation_model']:
                system_dict['computation_model'] = json.loads(system_dict['computation_model'])
            result.append(system_dict)

        return result

def get_unique_property_values(property_name: str) -> List[str]:
    """Get all unique values for a given property."""
    with get_db_connection() as conn:
        if property_name == "computation_model":
            # For JSON array fields, we need to extract unique values differently
            systems = conn.execute("SELECT computation_model FROM systems WHERE computation_model IS NOT NULL").fetchall()
            values = set()
            for row in systems:
                if row[0]:
                    models = json.loads(row[0])
                    values.update(models)
            return sorted(list(values))
        else:
            # For regular string fields
            values = conn.execute(f"""
                SELECT DISTINCT {property_name} FROM systems
                WHERE {property_name} IS NOT NULL
                ORDER BY {property_name}
            """).fetchall()
            return [row[0] for row in values]

def get_youtube_thumbnail(url: str) -> Optional[str]:
    """Extract YouTube thumbnail URL from video URL."""
    if not url:
        return None

    # YouTube video ID patterns - more precise matching
    patterns = [
        r'(?:youtube\.com/watch\?v=)([0-9A-Za-z_-]{11})(?:&|$)',  # youtube.com/watch?v=ID
        r'(?:youtube\.com/embed/)([0-9A-Za-z_-]{11})(?:\?|$)',    # youtube.com/embed/ID
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})(?:\?|$)',             # youtu.be/ID
        r'(?:youtube\.com/v/)([0-9A-Za-z_-]{11})(?:\?|$)',        # youtube.com/v/ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            # Validate video ID length (YouTube IDs are exactly 11 characters)
            if len(video_id) == 11:
                return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"

    return None