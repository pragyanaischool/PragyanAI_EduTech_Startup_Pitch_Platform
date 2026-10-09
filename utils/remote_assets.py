import os
from pathlib import Path
import urllib.request
import streamlit as st
from utils.secrets_helper import get_secret

# Local fallback cache directory
CACHE_DIR = Path("data/uploads")

# Fallback links if not overridden in secrets
DEFAULT_LOGO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200"
DEFAULT_DECK_VIEW = "https://drive.google.com/file/d/sample/view"
DEFAULT_DECK_DOWNLOAD = "https://raw.githubusercontent.com/pdf-association/pdf-examples/master/sample.pdf"
DEFAULT_FINANCIALS_VIEW = "https://docs.google.com/spreadsheets/d/sample/view"
DEFAULT_FINANCIALS_DOWNLOAD = "https://file-examples.com/storage/fe5546e72763f044e1388d0/2017/02/file_example_XLSX_50.xlsx"

def get_remote_links() -> dict:
    """Returns the configured remote asset URLs."""
    return {
        "logo_url": get_secret("REMOTE_LOGO_URL", DEFAULT_LOGO_URL),
        "deck_view_url": get_secret("REMOTE_DECK_VIEW_URL", DEFAULT_DECK_VIEW),
        "deck_download_url": get_secret("REMOTE_DECK_DOWNLOAD_URL", DEFAULT_DECK_DOWNLOAD),
        "financials_view_url": get_secret("REMOTE_FINANCIALS_VIEW_URL", DEFAULT_FINANCIALS_VIEW),
        "financials_download_url": get_secret("REMOTE_FINANCIALS_DOWNLOAD_URL", DEFAULT_FINANCIALS_DOWNLOAD),
    }

@st.cache_data(show_spinner=False)
def fetch_remote_file_bytes(url: str, local_subfolder: str, filename: str) -> bytes:
    """
    Downloads a remote file over HTTPS, caches it locally in data/uploads/<subfolder>/,
    and returns the file bytes.
    """
    target_dir = CACHE_DIR / local_subfolder
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / filename

    # Return cached local file if already downloaded
    if destination.exists() and destination.stat().st_size > 0:
        with open(destination, "rb") as f:
            return f.read()

    # Download from remote link
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()

        with open(destination, "wb") as f:
            f.write(content)

        return content
    except Exception as e:
        st.warning(f"Failed to fetch remote asset from {url}: {e}")
        return b""
