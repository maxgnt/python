from dataclasses import dataclass
from datetime import datetime


@dataclass
class SystemMetrics:
    timestamp: datetime
    hostname: str
    cpu_percent: float
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_usage: str

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "hostname": self.hostname,
            "cpu_percent": self.cpu_percent,
            "memory_total": self.memory_total,
            "memory_available": self.memory_available,
            "memory_percent": self.memory_percent,
            "disk_usage": self.disk_usage
        }

    def __str__(self):
        return (
            f"[{self.timestamp}] "
            f"CPU: {self.cpu_percent}% | "
            f"RAM: {self.memory_percent}%"
        )
