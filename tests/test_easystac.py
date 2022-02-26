import unittest

import xarray as xr
from geojson import Point, Polygon

import easystac as es
import easystac.planetary as pc

geom = Point([-76.1, 4.3])

geom2 = Polygon(
    [
        [
            [-122.1553, 38.7578],
            [-121.8321, 39.7444],
            [-123.0002, 39.7503],
            [-123.0002, 38.7609],
            [-122.1553, 38.7578],
        ]
    ]
)


class Test(unittest.TestCase):
    """Tests for the easystac package."""

    def test_general(self):
        """Test the general Image Collection"""
        result = (
            es.ImageCollection("HLSS30.v2.0")
            .fromSTAC("https://cmr.earthdata.nasa.gov/stac/LPCLOUD/")
            .filterBounds(geom2)
            .filterDate("2021-01-01", "2022-01-01")
            .getInfo(epsg=4326, resolution=0.0001, assets=["B02", "B03", "B04"])
        )
        self.assertIsInstance(result, xr.DataArray)

    def test_planetary(self):
        """Test the Planetary Computer extension"""
        result = (
            pc.ImageCollection("sentinel-2-l2a")
            .filterBounds(geom)
            .filterDate("2020-01-01", "2021-01-01")
            .getInfo(resolution=10)
        )
        self.assertIsInstance(result, xr.DataArray)


if __name__ == "__main__":
    unittest.main()
