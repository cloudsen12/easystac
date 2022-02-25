import json
import os
import warnings
from pathlib import Path

import planetary_computer as pc
import stackstac

from ..base import BaseImageCollection

warnings.simplefilter("always", UserWarning)


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
