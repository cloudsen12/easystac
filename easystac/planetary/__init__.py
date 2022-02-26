"""easystac - Planetary Computer authentication"""
import json
import os
import warnings
from pathlib import Path

from ..logging_utils import obtain_and_write_token
from .image_collection import ImageCollection

warnings.simplefilter("always", UserWarning)

CREDENTIAL_FILE = "~/.config/easystac/credentials_pc.json"


def Authenticate(token=None):
    """Generates an authentication prompt to Planetary Computer.

    Examples
    --------
    >>> import easystac.planetary as pc
    >>> pc.Authenticate()
    """
    if token is None:
        obtain_and_write_token(stac_server="pc")
    else:
        obtain_and_write_token(token, stac_server="pc")


def Initialize():
    """Initializes the authentication process for Planetary Computer.

    Examples
    --------
    >>> import easystac.planetary as pc
    >>> pc.Initialize()
    """
    credentials_path = Path(CREDENTIAL_FILE).expanduser()
    if credentials_path.is_file():
        credential = json.load(open(credentials_path))
        os.environ["PC_SDK_SUBSCRIPTION_KEY"] = credential["token"]
    else:
        warnings.warn(
            "PC_SDK_SUBSCRIPTION_KEY is not set.\n"
            + "If you are a registered user,"
            + " it is recommended to set your token for a more favorable rate limiting.\n"
            + "More info in https://planetarycomputer.microsoft.com/docs/concepts/sas/",
            UserWarning,
        )
