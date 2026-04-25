"""
ticket_manager.py
In-memory support ticket system.
Swap self._store with a real database (SQLite / PostgreSQL) in production.
"""

import uuid
import datetime
from typing import Optional


class TicketManager:

    SLA_MAP = {
        "Low":      "5 business days",
        "Medium":   "2 business days",
        "High":     "24 hours",
        "Critical": "4 hours",
    }

    TEAM_MAP = {
        "Display / Optics":          "display-team@apple-support.com",
        "Battery & Charging":        "hardware-team@apple-support.com",
        "Audio / Spatial Sound":     "audio-team@apple-support.com",
        "Eye / Hand Tracking":       "sensor-team@apple-support.com",
        "Software / Apps":           "software-team@apple-support.com",
        "Hardware Damage":           "repairs-team@apple-support.com",
        "Account & Billing":         "billing-team@apple-support.com",
        "AI Agent — Auto Created":   "escalations@apple-support.com",
        "Other":                     "general@apple-support.com",
    }

    def __init__(self):
        self._store: dict[str, dict] = {}

    def create(
        self,
        name:        str,
        email:       str,
        product:     str,
        category:    str,
        priority:    str,
        description: str,
        serial:      str = "",
        session_id:  Optional[str] = None,
    ) -> dict:
        tid = "AP-" + uuid.uuid4().hex[:6].upper()
        now = datetime.datetime.utcnow().isoformat()
        ticket = {
            "id":          tid,
            "name":        name,
            "email":       email,
            "product":     product,
            "serial":      serial or "N/A",
            "category":    category,
            "priority":    priority,
            "description": description,
            "status":      "Open",
            "session_id":  session_id,
            "sla":         self.SLA_MAP.get(priority, "2 business days"),
            "assigned_to": self.TEAM_MAP.get(category, "general@apple-support.com"),
            "created_at":  now,
            "updated_at":  now,
            "history": [
                {"action": "Ticket created", "by": "System", "at": now}
            ],
        }
        self._store[tid] = ticket
        print(f"   🎫 Ticket {tid} [{priority}] {product}")
        return ticket

    def get(self, ticket_id: str) -> Optional[dict]:
        return self._store.get(ticket_id)

    def list_all(self) -> list:
        return sorted(
            self._store.values(),
            key=lambda t: t["created_at"],
            reverse=True,
        )

    def stats(self) -> dict:
        all_t = list(self._store.values())
        return {
            "total":    len(all_t),
            "open":     sum(1 for t in all_t if t["status"] == "Open"),
            "resolved": sum(1 for t in all_t if t["status"] == "Resolved"),
        }
