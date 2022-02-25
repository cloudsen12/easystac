import json
import os

import stackstac

from ..base import BaseImageCollection


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
