"""easystac - Planetary Computer authentication"""
import json
import os
import warnings
from pathlib import Path

import stackstac

from ..base import BaseImageCollection
from ..logging_utils import obtain_and_write_token

warnings.simplefilter("always", UserWarning)

CREDENTIAL_FILE = "~/.config/easystac/credentials_planetary.json"


def Authenticate(token=None):
    if token is None:
        obtain_and_write_token(stac_server="pc")
    else:
        obtain_and_write_token(token, stac_server="pc")


def Initialize():
    """Initialize the package"""
    credentials_path = Path(CREDENTIAL_FILE).expanduser()
    if credentials_path.is_file():
        credential = json.load(open(credentials_path))
        os.environ["PC_SDK_SUBSCRIPTION_KEY"] = credential["token"]
    else:
        warnings.warn(
            "PC_SDK_SUBSCRIPTION_KEY is not set. "
            + "If you are a registered user,"
            + " it is recommended to set your token for a more favorable rate limiting."
            + " More info in https://planetarycomputer.microsoft.com/docs/concepts/sas/",
            UserWarning,
        )


class ImageCollection(BaseImageCollection):
    """ImageCollection object for Planetary Computer.

    This object mimics the Earth Engine filtering methods for ee.ImageCollection class and
    makes them available for the Planetary Computer STAC. Items signing is automatically
    done.

    Parameters
    ----------
    collection: str
        Collection name.

    Examples
    --------
    >>> import easystac.planetary as pc
    >>> from geojson import Point
    >>> pc.Authenticate()
    >>> pc.Initialize()
    >>> geom = Point([-76.1,4.3])
    >>> S2 = (pc.ImageCollection("sentinel-2-l2a")
            .filterBounds(geom)
            .filterDate("2020-01-01","2021-01-01")
            .getInfo(resolution = 10))
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
        >>> import easystac.planetary as pc
        >>> from geojson import Point
        >>> pc.Authenticate()
        >>> pc.Initialize()
        >>> geom = Point([-76.1,4.3])
        >>> S2 = (pc.ImageCollection("sentinel-2-l2a")
                .filterBounds(geom)
                .filterDate("2020-01-01","2021-01-01")
                .getInfo(resolution = 10))
        """
        parameters = None

        if "PC_SDK_SUBSCRIPTION_KEY" in os.environ:
            parameters = {"subscription-key": os.environ["PC_SDK_SUBSCRIPTION_KEY"]}

        search = self._search(
            url="https://planetarycomputer.microsoft.com/api/stac/v1",
            parameters=parameters,
        )

        items = [pc.sign(item).to_dict() for item in search.get_items()]

        image_collection = stackstac.stack(items, **kwargs)

        return image_collection
