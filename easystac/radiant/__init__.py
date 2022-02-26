"""easystac - RadiantML authentication"""
import json
import os
from pathlib import Path

import stackstac

from ..logging_utils import obtain_and_write_token
from .image_collection import ImageCollection

CREDENTIAL_FILE = "~/.config/easystac/credentials_radiant.json"


def Authenticate(token=None):
    """Generates an authentication prompt to Radiant ML Hub.

    Examples
    --------
    >>> import easystac.radiant as rd
    >>> rd.Authenticate()
    """
    if token is None:
        obtain_and_write_token(stac_server="radiant")
    else:
        obtain_and_write_token(token, stac_server="radiant")


def Initialize():
    """Initializes the authentication process for Radiant ML Hub.

    Examples
    --------
    >>> import easystac.radiant as rd
    >>> rd.Initialize()
    """
    credentials_path = Path(CREDENTIAL_FILE).expanduser()
    if credentials_path.is_file():
        credential = json.load(open(credentials_path))
        os.environ["MLHUB_API_KEY"] = credential["token"]
    else:
        raise Exception(
            "Please authorize access to your radiantHub account by "
            "running:: \n\n>>> import easystac.radiant as rd\n"
            ">>> rd.Authenticate()\n"
        )
