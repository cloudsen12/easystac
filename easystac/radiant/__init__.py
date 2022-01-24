"""easystac - RadiantML authentification"""
import json
import os
from pathlib import Path

from ..logging_utils import obtain_and_write_token

CREDENTIAL_FILE = "~/.config/easystac/credentials_radiant.json"


def Authenticate(token=None):
    if token is None:
        obtain_and_write_token(stac_server="radiant")
    else:
        obtain_and_write_token(token, stac_server="radiant")


def Initialize():
    """Initialize the package"""
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
