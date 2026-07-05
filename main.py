"""
Entry point: scrape all JCR house pages, then filter/display/export.

Usage:
    python main.py
"""
from scraper import make_session, scrape_all_houses
from filters import filter_rooms, print_table, save_to_csv

# --- Fill in your cookies here (see README.md for how to get them) ---
COOKIE_CONTROL = 'CookieControlValueHere'
SESSION_COOKIE = "SessionCookieValueHere"


def main():
    session = make_session(COOKIE_CONTROL, SESSION_COOKIE)
    rooms = scrape_all_houses(session)

    print(f"\nScraped {len(rooms)} available rooms total.\n")

    save_to_csv(rooms, "jcr_rooms_all.csv")

#Use filter to filter rooms based on criteria, e.g., has_shower=True, has_double_bed=False

if __name__ == "__main__":
    main()