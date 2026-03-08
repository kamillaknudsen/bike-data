# Copilot instructions for bike-data

Purpose: quick reference for AI coding agents to get productive in this repository.

Big picture
- This repo collects shared micromobility vehicle snapshots, stores them as daily CSVs, and provides a simple visualization script.
- Data flow: API -> per-run Python scripts (`download_data.py`, `hub_data.py`) -> CSV files in `data/` -> analysis in `basic_heatmap.py` which reads `data/bikes_*.csv`.

Key files & responsibilities
- `download_data.py` — main working example for harvesting vehicle data from `https://api.datadeelmobiliteit.nl/vehicles`. It:
  - Parses `json["data"]["vehicles"]` and `json["last_updated"]`.
  - Appends rows to `data/bikes_YYYY-MM-DD.csv` and writes a header when creating the file.
  - CSV columns: `timestamp, system_id, vehicle_id, lat, lon, is_reserved, is_disabled, form_factor, propulsion_type`.
- `hub_data.py` — intended to fetch stop/hub data (URL: `https://mds.dashboarddeelmobiliteit.nl/stops?municipality=GM0363`). Currently incomplete and has indentation/variable issues; treat it as an implementation TODO.
- `basic_heatmap.py` — reads all `data/bikes_*.csv`, concatenates them, filters to Rotterdam bounding box (lat 51.837–51.998, lon 4.256–4.712), drops disabled bikes, and plots a KDE heatmap with a `contextily` basemap.

Project conventions & patterns (explicit, discoverable)
- Data files are named with the pattern `data/bikes_YYYY-MM-DD.csv` (downloaded from `download_data.py`). Hub files are expected under `data/hubs/hubs_YYYY-MM-DD.csv`.
- Scripts append to CSVs (open with mode `a`) and add a header only when the file does not exist. Follow this pattern when adding new harvesting scripts.
- Time handling: API returns an ISO timestamp (e.g. `last_updated` with trailing `Z`). Existing code converts `Z` to `+00:00` before `datetime.fromisoformat`.
- Spatial filtering: `basic_heatmap.py` filters by explicit lat/lon bounds for Rotterdam. Reuse these constants when adding regional analyses.
- Minimal error handling: scripts wrap network and file operations in a try/except and print exceptions; there are no tests or CI configured.

External dependencies (from imports)
- runtime: `requests`
- analysis/plotting: `pandas`, `matplotlib`, `seaborn`, `contextily`
- standard library: `csv`, `datetime`, `os`, `glob`

Running & developer workflows (discoverable)
- Scripts are standalone Python files. Typical usage:
  - Harvest vehicles: `python download_data.py`
  - Harvest hubs (work-in-progress): `python hub_data.py`
  - Visualize: `python basic_heatmap.py`
- There is no requirements.txt or virtualenv config; create one if reproducing the environment. Prefer installing packages used by the imports above.
- For periodic data collection, run `download_data.py` on a scheduler (cron, systemd timer) — script is idempotent in the sense it appends daily CSV rows.

Implementation notes & known issues
- `hub_data.py` is incomplete: variable names like `vehicles`, `timestamp_str`, `time_str` are used but not defined; CSV path `data/hubs/` may not be created; indentation and empty dicts indicate an unfinished implementation. Treat this file as a TODO when making changes.
- `basic_heatmap.py` assumes all `data/bikes_*.csv` files share the same columns; follow the exact header format when updating harvesting scripts.

If something here is unclear or you'd like the instructions to be expanded with examples of fixes (for example a corrected `hub_data.py`) or a `requirements.txt`, say which area to expand and I will update the file.
