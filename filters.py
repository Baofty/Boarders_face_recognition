"""
Simple filtering and display helpers for lists of Room objects.
"""
import csv
from models import Room


def filter_rooms(
    rooms: list[Room],
    has_shower: bool = None,
    has_double_bed: bool = None,
    has_en_suite: bool = None,
    has_fridge: bool = None,
    has_bath: bool = None,
    is_set: bool = None,
    is_bedsit: bool = None,
    location: str = None,
    rent_band: str = None,
) -> list[Room]:
    """Filter rooms by any combination of attributes.

    Pass only the filters you care about; leave the rest as None to ignore them.
    Example: filter_rooms(rooms, has_shower=True, has_double_bed=False)
    """
    result = rooms

    checks = {
        "has_shower": has_shower,
        "has_double_bed": has_double_bed,
        "has_en_suite": has_en_suite,
        "has_fridge": has_fridge,
        "has_bath": has_bath,
        "is_set": is_set,
        "is_bedsit": is_bedsit,
    }

    for attr, expected in checks.items():
        if expected is not None:
            result = [r for r in result if getattr(r, attr) == expected]

    if location is not None:
        result = [r for r in result if r.location.lower() == location.lower()]

    if rent_band is not None:
        result = [r for r in result if r.rent_band.lower() == rent_band.lower()]

    return result


def print_table(rooms: list[Room]) -> None:
    """Print rooms as a readable table in the terminal."""
    if not rooms:
        print("No rooms match.")
        return

    headers = ["Location", "Room", "Band", "Layout", "DblBed", "En-suite", "Shower", "Fridge"]
    rows = [
        [
            r.location,
            r.room_name,
            r.rent_band,
            "Set" if r.is_set else "Bedsit" if r.is_bedsit else "?",
            "Y" if r.has_double_bed else "N",
            "Y" if r.has_en_suite else "N",
            "Y" if r.has_shower else "N",
            "Y" if r.has_fridge else "N",
        ]
        for r in rooms
    ]

    widths = [max(len(str(x)) for x in [h] + [row[i] for row in rows]) for i, h in enumerate(headers)]

    def fmt_row(row):
        return " | ".join(str(v).ljust(w) for v, w in zip(row, widths))

    print(fmt_row(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt_row(row))


def save_to_csv(rooms: list[Room], filename: str = "jcr_rooms_all.csv") -> None:
    if not rooms:
        print("No rooms to save.")
        return

    fieldnames = list(rooms[0].to_dict().keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for room in rooms:
            writer.writerow(room.to_dict())

    print(f"Saved {len(rooms)} rooms to {filename}")