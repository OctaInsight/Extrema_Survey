"""
Supabase connection helper for the EXTREMA partner survey.

Reads credentials from Streamlit secrets (.streamlit/secrets.toml), using the
same block as the existing HARMONIA app so one project serves both:

    [supabase]
    url = "https://xxxxxxxx.supabase.co"
    key = "your-anon-public-key"

    # Optional. Add this if you used Option A in supabase_schema.sql, where the
    # anon key may INSERT but not SELECT. The coordinator page reads with it.
    service_key = "your-service-role-key"

If `service_key` is absent the anon key is used for reads too, which matches the
HARMONIA setup and requires Option B in the schema.

With no [supabase] block at all the module writes to data/responses.csv, so the
app runs locally without touching the live database.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pandas as pd
import streamlit as st

TABLE_NAME = "extrema_needs_survey"

DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "responses.csv"

# Column order in Postgres. Anything not listed is folded into `raw`, so adding
# a question to content.py never needs a migration.
DB_COLUMNS = [
    "response_ref", "created_at", "partner_code", "partner_name", "country",
    "partner_group", "respondent", "role", "email",
    "n1", "n2", "n3", "n4", "n5", "n6", "n7",
    "cap_tech", "cap_data", "cap_inst", "cap_eu",
    "financing", "funding_routes", "discontinued_pilot", "discontinued_why",
    "assets", "heritage_types", "hazards", "permit_body", "existing_plans",
    "mission_charter", "heritage_fte", "components", "trl", "prior_demonstration",
    "biggest_barrier", "comments",
]

SCORE_COLUMNS = [
    "n1", "n2", "n3", "n4", "n5", "n6", "n7",
    "cap_tech", "cap_data", "cap_inst", "cap_eu",
]

# Survey field name -> database column name.
FIELD_MAP = {
    "response_id": "response_ref",
    "submitted_at": "created_at",
    "group": "partner_group",
    "N1": "n1", "N2": "n2", "N3": "n3", "N4": "n4",
    "N5": "n5", "N6": "n6", "N7": "n7",
    "CAP_TECH": "cap_tech", "CAP_DATA": "cap_data",
    "CAP_INST": "cap_inst", "CAP_EU": "cap_eu",
}
REVERSE_MAP = {v: k for k, v in FIELD_MAP.items()}


class StorageError(RuntimeError):
    """Raised when a write fails and the caller must tell the respondent."""


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
def _secrets() -> dict:
    try:
        return dict(st.secrets.get("supabase", {}))
    except Exception:  # noqa: BLE001 — no secrets file at all
        return {}


def supabase_configured() -> bool:
    s = _secrets()
    return bool(s.get("url") and s.get("key"))


def _import_supabase():
    """Import the client library, with a message that says how to fix it.

    Imported here rather than at module level so a missing dependency shows a
    readable message instead of crashing the whole app on startup.
    """
    try:
        from supabase import create_client  # noqa: PLC0415
    except ModuleNotFoundError as exc:  # noqa: BLE001
        raise StorageError(
            "The `supabase` package is not installed in this environment. "
            "Check that requirements.txt sits in the repository root next to app.py, "
            "that it contains a line reading `supabase>=2.10`, and that it is "
            "committed and pushed. Then use Manage app > Reboot on Streamlit Cloud "
            "so the environment is rebuilt."
        ) from exc
    return create_client


@st.cache_resource(show_spinner=False)
def get_client(role: str = "anon"):
    """Cached Supabase client. role is 'anon' (writes) or 'service' (reads)."""
    create_client = _import_supabase()
    s = _secrets()
    url = s.get("url")
    if role == "service":
        key = s.get("service_key") or s.get("key")
    else:
        key = s.get("key")
    if not url or not key:
        raise StorageError("Supabase url or key missing from secrets.")
    return create_client(url, key)


def supabase_installed() -> bool:
    import importlib.util  # noqa: PLC0415

    return importlib.util.find_spec("supabase") is not None


def backend_name() -> str:
    if not supabase_configured():
        return "local CSV"
    return "Supabase" if supabase_installed() else "Supabase (package missing)"


def stamp() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------
def _to_db_row(row: dict) -> dict:
    known, extra = {}, {}
    for k, v in row.items():
        col = FIELD_MAP.get(k, k)
        if col in DB_COLUMNS:
            known[col] = v
        else:
            extra[k] = v
    known["raw"] = extra or None
    for col in SCORE_COLUMNS:
        if known.get(col) is not None:
            known[col] = int(known[col])
    return known


def insert_response(data: dict) -> None:
    """Insert one survey response. Raises on failure so the caller can show an error."""
    get_client("anon").table(TABLE_NAME).insert(_to_db_row(data)).execute()


def save_response(row: dict) -> None:
    """Persist one response, keeping a local copy if the database refuses it."""
    if not supabase_configured():
        _write_csv(row)
        return
    try:
        insert_response(row)
        fetch_responses.clear()
    except Exception as exc:  # noqa: BLE001
        _write_csv(row)  # keep the answer rather than lose it
        raise StorageError(
            f"The database rejected the submission ({exc}). A local copy was kept; "
            "please tell the coordinator."
        ) from exc


def _write_csv(row: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(
        CSV_PATH, mode="a", header=not CSV_PATH.exists(), index=False
    )
    fetch_responses.clear()


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
@st.cache_data(ttl=30, show_spinner=False)
def fetch_responses() -> pd.DataFrame:
    """All responses as a DataFrame, using the survey-side column names."""
    if not supabase_configured():
        return pd.read_csv(CSV_PATH) if CSV_PATH.exists() else pd.DataFrame()
    try:
        res = (
            get_client("service")
            .table(TABLE_NAME)
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        df = pd.DataFrame(res.data or [])
        if df.empty:
            return df
        if "raw" in df.columns:
            extras = pd.json_normalize(df["raw"].apply(lambda x: x or {}))
            df = pd.concat([df.drop(columns=["raw"]), extras], axis=1)
        return df.rename(columns=REVERSE_MAP)
    except StorageError as exc:
        st.error(str(exc))
        return pd.DataFrame()
    except Exception as exc:  # noqa: BLE001
        st.error(
            f"Could not read from Supabase ({exc}). If you used Option A in the schema, "
            "add `service_key` to your secrets; the anon key cannot read that table."
        )
        return pd.DataFrame()


def connection_check() -> tuple[bool, str]:
    """Status line for the coordinator page."""
    if not supabase_configured():
        return False, "No Supabase secrets found — writing to data/responses.csv."
    reading_with = "service-role key" if _secrets().get("service_key") else "anon key"
    try:
        res = (
            get_client("service")
            .table(TABLE_NAME)
            .select("response_ref", count="exact")
            .limit(1)
            .execute()
        )
        return True, (
            f"Connected to Supabase, reading `{TABLE_NAME}` with the {reading_with}. "
            f"{res.count} row(s)."
        )
    except StorageError as exc:
        return False, str(exc)
    except Exception as exc:  # noqa: BLE001
        return False, f"Could not reach `{TABLE_NAME}` ({exc})."


def export_json(df: pd.DataFrame) -> str:
    return json.dumps(
        json.loads(df.to_json(orient="records", date_format="iso")),
        indent=2,
        ensure_ascii=False,
    )
