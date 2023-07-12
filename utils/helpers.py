from pathlib import Path
from typing import Tuple

ROOT_DIR = Path(__file__).parent.parent
PROGRESS_FILE = ROOT_DIR / "progress.txt"


def build_url_with_params(url: str, params: dict) -> str:
    """
    Builds a URL with the given parameters.

    Args:
        url (str): The URL to build.
        params (dict): The parameters to add to the URL.

    Returns:
        str: The built URL.
    """

    # if url includes ? only add the parameters with & between them

    if "?" in url:
        return url + "&" + "&".join([f"{key}={value}" for key, v in params.items() for value in v])

    return url + "?" + "&".join([f"{key}={value}" for key, v in params.items() for value in v])


def get_latest_state() -> Tuple[int, int]:
    """
    Gets the lastest page number from the progress.txt file.

    Returns:
        tuple: A tuple of page number and page count.
    """
    try:
        with open(PROGRESS_FILE, "r") as f:
            text = f.read()
            return int(text.split(",")[0].split("=")[1]), int(text.split(",")[1].split("=")[1])
    except FileNotFoundError:
        return 0, 0


def set_latest_state(page_number: int, page_count: int) -> bool:
    """
    Sets the lastest page number to the progress.txt file.

    Args:
        page_number (int): The page number to set.
    """
    try:
        with open(PROGRESS_FILE, "w") as f:
            f.write(f"page_number={page_number},page_count={page_count}")
        return True
    except Exception as e:
        return False
