import sqlite3
from datetime import datetime, timedelta

class MetricsDatabase:
    def __init__(self, db_path="syswatch.db"):
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    hostname TEXT,
                    cpu_percent REAL,
                    memory_percent REAL,
                    memory_total INTEGER,
                    memory_available INTEGER,
                    disk_usage TEXT
                )
            """)

    def save(self, metrics):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO metrics (
                    timestamp, hostname, cpu_percent,
                    memory_percent, memory_total,
                    memory_available, disk_usage
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                metrics.timestamp.isoformat(),
                metrics.hostname,
                metrics.cpu_percent,
                metrics.memory_percent,
                metrics.memory_total,
                metrics.memory_available,
                metrics.disk_usage
            ))
