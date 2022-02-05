"""easystac - RadiantML authentication"""
import json
import os
from pathlib import Path

import stackstac

from ..base import BaseImageCollection
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


class ImageCollection(BaseImageCollection):
    """ImageCollection object for Radiant Earth ML Hub.

    This object mimics the Earth Engine filtering methods for ee.ImageCollection class and
    makes them available for the Radiant Earth ML Hub STAC.

    Parameters
    ----------
    collection: str
        Collection name.

    Examples
    --------
    >>> import easystac.radiant as rd
    >>> rd.Authenticate()
    >>> rd.Initialize()
    >>> S1floods = (rd.ImageCollection("sen12floods_s1_source")
            .filterDate("2019-01-01","2019-01-05")
            .getInfo(epsg = 4326,resolution = 0.0001))
    """

    def getInfo(self, **kwargs):
        """Returns all the information from the STAC search.

        Parameters
        ----------
        **kwargs
            Additional arguments passed to :code:`stackstac.stack()`. Some of them are
            :code:`epsg`, :code:`resolution`, and :code:`bbox`.

        Returns
        -------
        xarray.DataArray
            Chunked DataArray with Dask.

        Examples
        --------
        >>> import easystac.radiant as rd
        >>> rd.Authenticate()
        >>> rd.Initialize()
        >>> S1floods = (rd.ImageCollection("sen12floods_s1_source")
                .filterDate("2019-01-01","2019-01-05")
                .getInfo(epsg = 4326,resolution = 0.0001))
        """
        search = self._search(
            url="https://api.radiant.earth/mlhub/v1/",
            parameters={"key": os.environ["MLHUB_API_KEY"]},
        )

        items = [item.to_dict() for item in search.get_items()]

        image_collection = stackstac.stack(items, **kwargs)

        return image_collection
