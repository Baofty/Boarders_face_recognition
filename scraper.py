"""
Scraping logic for the Magdalene Rooms Ballot site.

Handles authenticated requests (via cookies) and parsing of the
house.php pages into Room objects.
"""
import re
import requests
from bs4 import BeautifulSoup

from models import Room

BASE_URL = "https://roomsballot.magd.cam.ac.uk"

HOUSE_IDS = {
    2: "Basing House",
    3: "Benson Court",
    4: "23 Bridge Street",
    5: "30 Bridge Street",
    7: "Buckingham Court",
    9: "5 Chesterton Road",
    14: "Cripps Court",
    15: "Edwards Court",
    16: "First Court",
    21: "Mallory Court",
    25: "Old Lodge",
    27: "30 Thompson's Lane",
    29: "34 Thompson's Lane",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def make_session(cookie_control: str, session_cookie: str) -> requests.Session:
    """Build a requests.Session pre-loaded with the auth cookies.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update({
        "CookieControl": cookie_control,
        "mod_auth_openidc_session": session_cookie,
    })
    return session


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def yes_no(value: str) -> bool:
    return value.strip().lower() == "yes"


def get_soup(session: requests.Session, url: str):
    response = session.get(url, timeout=20, allow_redirects=True)

    if "accounts.google.com" in response.url:
        raise RuntimeError(
            "Not authenticated: redirected to Google sign-in. "
            "Your cookies are missing or expired -- refresh them from the browser."
        )

    return BeautifulSoup(response.text, "html.parser"), response


def parse_list_group(ul) -> dict:
    data = {}
    for li in ul.find_all("li", class_="list-group-item"):
        label = li.find("label")
        if not label:
            continue
        key = clean_text(label.get_text()).rstrip(":")
        label.extract()
        value = clean_text(li.get_text(" ", strip=True))
        data[key] = value
    return data


def get_modal_attributes(soup, modal_id: str) -> dict:
    attrs = {}
    if not modal_id:
        return attrs

    modal = soup.find("div", id=modal_id)
    if not modal:
        return attrs

    for ul in modal.find_all("ul", class_="list-group"):
        attrs.update(parse_list_group(ul))

    return attrs


def build_room(location: str, room_name: str, attributes: dict) -> Room:
    set_or_bedsit = attributes.get("Set or Bedsit", "")

    return Room(
        location=location,
        room_name=room_name,
        status=attributes.get("Status", ""),
        allocation=attributes.get("Allocation", ""),
        rent_band=attributes.get("Rent Band", ""),
        floor=attributes.get("Floor", ""),
        set_or_bedsit=set_or_bedsit,
        remarks=attributes.get("Remarks", ""),

        is_set=set_or_bedsit.lower() == "set",
        is_bedsit=set_or_bedsit.lower() == "bedsit",

        has_double_bed=yes_no(attributes.get("Double Bed", "")),
        has_en_suite=yes_no(attributes.get("En-suite", "")),
        has_fridge=yes_no(attributes.get("Fridge", "")),
        has_bath=yes_no(attributes.get("Bath", "")),
        has_shower=yes_no(attributes.get("Shower", "")),
        has_washbasin=yes_no(attributes.get("Washbasin", "")),
        has_low_ceiling=yes_no(attributes.get("Low Ceiling", "")),
        has_attic=yes_no(attributes.get("Attic", "")),
        has_steep_staircase=yes_no(attributes.get("Steep Staircase", "")),

        conference_room_level=attributes.get("Conference Room", ""),
    )


def scrape_house(session: requests.Session, house_id: int, expected_location: str) -> list[Room]:
    url = f"{BASE_URL}/house.php?id={house_id}"
    soup, response = get_soup(session, url)

    print(f"Scanning {expected_location}: {response.status_code} {response.url}")

    rooms = []
    room_divs = soup.select("div.col-xl-3.col-lg-6.col-md-6.col-sm-12.col-12")

    for room_div in room_divs:
        figcaption = room_div.find("figcaption", class_="figure-caption")
        if not figcaption:
            continue

        title = figcaption.find("h4", class_="figure-title")
        room_name = clean_text(title.get_text()) if title else ""

        info_link = room_div.find("a", attrs={"data-toggle": "modal"})
        modal_target = info_link.get("data-target") if info_link else None
        modal_id = modal_target[1:] if modal_target and modal_target.startswith("#") else None

        attributes = get_modal_attributes(soup, modal_id)
        room = build_room(expected_location, room_name, attributes)

        if room.is_available():
            rooms.append(room)

    return rooms


def scrape_all_houses(session: requests.Session, house_ids: dict = None) -> list[Room]:
    house_ids = house_ids or HOUSE_IDS
    all_rooms = []

    for house_id, location_name in house_ids.items():
        try:
            house_rooms = scrape_house(session, house_id, location_name)
            print(f"  Found {len(house_rooms)} available rooms in {location_name}")
            all_rooms.extend(house_rooms)
        except Exception as e:
            print(f"  Error scraping {location_name} (id={house_id}): {e}")

    return all_rooms