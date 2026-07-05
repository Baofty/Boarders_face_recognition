"""
Room data model for the Magdalene Rooms Ballot scraper.
"""
from dataclasses import dataclass, asdict


@dataclass
class Room:
    """Represents a single room scraped from the rooms ballot site.

    Using a dataclass instead of a plain dict gives us:
      - Named, typed fields (e.g. has_double_bed: bool) instead of
        unlabeled "yes"/"no" strings in a dict.
      - Auto-generated __init__, __repr__, and __eq__ -- no boilerplate.
      - Editor autocomplete: typing `room.` shows every real attribute.
      - Easy conversion back to a dict (asdict) for CSV/JSON export.
    """
    location: str
    room_name: str
    status: str = ""
    allocation: str = ""
    rent_band: str = ""
    floor: str = ""
    set_or_bedsit: str = ""
    remarks: str = ""

    is_set: bool = False
    is_bedsit: bool = False

    has_double_bed: bool = False
    has_en_suite: bool = False
    has_fridge: bool = False
    has_bath: bool = False
    has_shower: bool = False
    has_washbasin: bool = False
    has_low_ceiling: bool = False
    has_attic: bool = False
    has_steep_staircase: bool = False

    conference_room_level: str = ""

    def is_available(self) -> bool:
        return self.status.lower() == "available"

    def summary(self) -> str:
        features = []
        features.append("Set" if self.is_set else "Bedsit" if self.is_bedsit else "Unknown layout")
        features.append("double bed" if self.has_double_bed else "no double bed")
        if self.has_en_suite:
            features.append("en-suite")
        if self.has_fridge:
            features.append("fridge")
        if self.has_shower:
            features.append("shower")
        return f"{self.room_name} ({self.location}) - Band {self.rent_band} - " + ", ".join(features)

    def to_dict(self) -> dict:
        return asdict(self)