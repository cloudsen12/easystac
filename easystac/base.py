from pystac_client import Client

import stackstac


class BaseImageCollection:
    """BaseImageCollection object.

    Base object for ImageCollection objects. This object mimics the Earth Engine
    filtering methods for ee.ImageCollection class and makes them available for other
    STAC.

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

    def __init__(self, collection):
        """Initializes the BaseImageCollection object."""

        self.collection = collection
        self.datetime = None
        self.geometry = None

    def filterDate(self, initialDate, finalDate):
        """Initializes the initial and final date for datetime filtering.

        Parameters
        ----------
        initialDate: str
            Initial date in format %Y-%m-%d.
        finalDate: str
            Final date in format %Y-%m-%d.

        Returns
        -------
        BaseImageCollection

        Examples
        --------
        >>> import easystac.planetary as pc
        >>> pc.Authenticate()
        >>> pc.Initialize()
        >>> S2 = (pc.ImageCollection("sentinel-2-l2a")
                .filterDate("2020-01-01","2021-01-01"))
        """
        self.datetime = f"{initialDate}/{finalDate}"

        return self

    def filterBounds(self, geometry):
        """Initializes the geometry for bounds filtering.

        Parameters
        ----------
        geometry: dict
            GeoJSON object of dictionary-like object representing a GeoJSON.

        Returns
        -------
        BaseImageCollection

        Examples
        --------
        >>> import easystac.planetary as pc
        >>> from geojson import Point
        >>> pc.Authenticate()
        >>> pc.Initialize()
        >>> geom = Point([-76.1,4.3])
        >>> S2 = (pc.ImageCollection("sentinel-2-l2a")
                .filterBounds(geom))
        """
        self.geometry = geometry

        return self

    def _search(self, url, parameters=None):
        """Computes the searching process through the STAC catalog.

        Parameters
        ----------
        url: str
            STAC Catalog url.
        parameters: dict
            Dictionary of query parameters.

        Returns
        -------
        ItemSearch
        """
        catalog = Client.open(url, parameters=parameters)

        search = catalog.search(
            intersects=self.geometry,
            datetime=self.datetime,
            collections=[self.collection],
        )

        return search


class ImageCollection(BaseImageCollection):
    """ImageCollection object for any kind of STAC.

    This object mimics the Earth Engine filtering methods for ee.ImageCollection class and
    makes them available for any kind of STAC.

    Parameters
    ----------
    collection: str
        Collection name.

    Examples
    --------
    >>> import easystac as es
    >>> from geojson import Polygon
    >>> geom = Polygon([
    >>>         [
    >>>             [-122.1553, 38.7578],
    >>>             [-121.8321, 39.7444],
    >>>             [-123.0002, 39.7503],
    >>>             [-123.0002, 38.7609],
    >>>             [-122.1553, 38.7578]
    >>>         ]
    >>>     ]
    >>> )
    >>> HLSS30 = (es.ImageCollection("HLSS30.v2.0")
    >>>     .fromSTAC("https://cmr.earthdata.nasa.gov/stac/LPCLOUD/")
    >>>     .filterBounds(geom)
    >>>     .filterDate("2021-01-01","2022-01-01")
    >>>     .getInfo(epsg = 4326,resolution = 0.0001,assets = ["B02","B03","B04"]))
    """

    def fromSTAC(self, url):
        """Initializes the STAC for querying.

        Parameters
        ----------
        url: str
            STAC Catalog url.

        Returns
        -------
        ImageCollection

        Examples
        --------
        >>> import easystac as es
        >>> HLSS30 = (es.ImageCollection("HLSS30.v2.0")
        >>>     .fromSTAC("https://cmr.earthdata.nasa.gov/stac/LPCLOUD/")
        """
        self.stac = url

        return self

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
        >>> import easystac as es
        >>> from geojson import Polygon
        >>> geom = Polygon([
        >>>         [
        >>>             [-122.1553, 38.7578],
        >>>             [-121.8321, 39.7444],
        >>>             [-123.0002, 39.7503],
        >>>             [-123.0002, 38.7609],
        >>>             [-122.1553, 38.7578]
        >>>         ]
        >>>     ]
        >>> )
        >>> HLSS30 = (es.ImageCollection("HLSS30.v2.0")
        >>>     .fromSTAC("https://cmr.earthdata.nasa.gov/stac/LPCLOUD/")
        >>>     .filterBounds(geom)
        >>>     .filterDate("2021-01-01","2022-01-01")
        >>>     .getInfo(epsg = 4326,resolution = 0.0001,assets = ["B02","B03","B04"]))
        """
        search = self._search(url=self.stac)

        items = [item.to_dict() for item in search.get_items()]

        image_collection = stackstac.stack(items, **kwargs)

        return image_collection
