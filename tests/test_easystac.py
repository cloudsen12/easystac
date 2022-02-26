import unittest

import xarray as xr
from geojson import Point

import easystac.planetary as pc

geom = Point([-76.1, 4.3])


class Test(unittest.TestCase):
    """Tests for the easystac package."""

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
