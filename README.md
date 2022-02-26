<p align="center">
  <a href="https://github.com/cloudsen12/easystac"><img src="https://raw.githubusercontent.com/cloudsen12/easystac/main/docs/_static/easystac.png" alt="easystac"></a>
</p>
<p align="center">
    <em>A Python package for simple STAC queries</em>
</p>

<p align="center">
<a href='https://pypi.python.org/pypi/easystac'>
    <img src='https://img.shields.io/pypi/v/easystac.svg' alt='PyPI' />
</a>
<a href='https://anaconda.org/conda-forge/easystac'>
    <img src='https://img.shields.io/conda/vn/conda-forge/easystac.svg' alt='conda-forge' />
</a>
<a href='https://easystac.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/easystac/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/cloudsen12/easystac/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/cloudsen12/easystac/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href="https://github.com/sponsors/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-Donate-ff69b4.svg" alt="GitHub Sponsors">
</a>
<a href="https://www.buymeacoffee.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-ff69b4.svg" alt="Buy me a coffee">
</a>
<a href="https://ko-fi.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/kofi-Donate-ff69b4.svg" alt="Ko-fi">
</a>
<a href="https://twitter.com/dmlmont" target="_blank">
    <img src="https://img.shields.io/twitter/follow/dmlmont?style=social" alt="Twitter">
</a>
<a href="https://twitter.com/csaybar" target="_blank">
    <img src="https://img.shields.io/twitter/follow/csaybar?style=social" alt="Twitter">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/cloudsen12/easystac](https://github.com/cloudsen12/easystac)

**Documentation**: [https://easystac.readthedocs.io/](https://easystac.readthedocs.io/)

**PyPI**: [https://pypi.org/project/easystac/](https://pypi.org/project/easystac/)

**Conda-forge**: [https://anaconda.org/conda-forge/easystac](https://anaconda.org/conda-forge/easystac)

---

## Overview

[SpatioTemporal Asset Catalogs (STAC)](https://stacspec.org/) provide a standardized format that describes
geospatial information. Multiple platforms are using this standard to provide clients several datasets.
Platforms such as [Planetary Computer](https://planetarycomputer.microsoft.com/),
[Radiant ML Hub](https://mlhub.earth/) and [Google Earth Engine](https://earthengine.google.com/) use this standard,
however, only Google Earth Engine provides a fully easy API that is transparent for clients.

`easystac` is a Python package that provides clients from Planetary Computer and Radiant ML Hub
with an easy API that is transparent for them, implementing Google Earth Engine-like methods
and classes to query, explore and convert STAC assets to [`xarray`](https://docs.xarray.dev/en/stable/) objects.

Some of the `easystac` features are listed here:

- Simple authentication for Planetary Computer and Radiant ML Hub.
- Access to STAC collections from Planetary Computer and Radiant ML Hub.
- Earth Engine-like classes such as ImageCollection, including filtering methods.
- Compatibility with xarray.

Check the simple usage of `easystac` here:

```python
import easystac as es
from geojson import Polygon

geom = Polygon([
        [
            [-122.1553, 38.7578],
            [-121.8321, 39.7444],
            [-123.0002, 39.7503],
            [-123.0002, 38.7609],
            [-122.1553, 38.7578]
        ]
    ]
)

HLSS30 = (es.ImageCollection("HLSS30.v2.0")
    .fromSTAC("https://cmr.earthdata.nasa.gov/stac/LPCLOUD/")
    .filterBounds(geom)
    .filterDate("2021-01-01","2022-01-01")
    .getInfo(epsg = 4326,resolution = 0.0001,assets = ["B02","B03","B04"]))
```

In the case of specialized STAC objects, we have created special modules for Planetary Computer:

```python
import easystac.planetary as pc
from geojson import Point

pc.Authenticate()
pc.Initialize()

geom = Point([-76.1,4.3])

S2 = (pc.ImageCollection("sentinel-2-l2a")
    .filterBounds(geom)
    .filterDate("2020-01-01","2021-01-01")
    .getInfo(resolution = 10))
```

This principle applies also for Radiant ML Hub.

```python
import easystac.radiant as rd

rd.Authenticate()
rd.Initialize()

S1floods = (rd.ImageCollection("sen12floods_s1_source")
    .filterDate("2019-01-01","2019-01-05")
    .getInfo(epsg = 4326,resolution = 0.0001))
```

## Installation

Install the latest version from PyPI:

```
pip install easystac
```

Upgrade `easystac` by running:

```
pip install -U easystac
```

Install the latest version from conda-forge:

```
conda install -c conda-forge easystac
```

Install the latest dev version from GitHub by running:

```
pip install git+https://github.com/cloudsen12/easystac
```

## License

The project is licensed under the MIT license.
