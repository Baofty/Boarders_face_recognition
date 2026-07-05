# Boarding House Face Recognition

A Tkinter + OpenCV + face_recognition app for managing boarding-house
students and recognizing them live via webcam, backed by a MySQL
database.

## File layout

| File | Responsibility |
|---|---|
| `config.py` | App-wide settings, reads DB credentials from env vars |
| `database.py` | All MySQL access (`Database` class) |
| `simple_facerec.py` | Face encoding/recognition wrapper (`SimpleFacerec`) |
| `camera.py` | Background webcam loop that draws recognized faces |
| `gui.py` | Tkinter UI (`BoardingHouseApp`) for add/remove/view students |
| `main.py` | Entry point wiring everything together |

## Setup

1. Install dependencies: `pip install -r requirements.txt` (If download fails for face_recognition, download wheel using https://github.com/z-mahmud22/Dlib_Windows_Python3.x and proceed with the rest of downloads)
2. Set DB credentials via environment variables (optional, defaults to
   `localhost`/`root`/no password):
   - `BH_DB_HOST`, `BH_DB_USER`, `BH_DB_PORT`, `BH_DB_NAME`, `BH_DB_PASSWORD`
3. Place a MySQL `boarders` table (`Name`, `In_House`) and optional
   `visitors` table (`Name`) in the `Boarding_House` schema.
4. Put reference student photos (named `<StudentName>.jpg/.png/.jpeg`)
   in an `images/` folder next to `main.py`.
5. Run: `python main.py`

