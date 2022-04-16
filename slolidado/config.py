"""
Slovenian lidar data downloader (SloLiDaDo)
Author: Žiga Maroh
2022
"""
from dataclasses import dataclass
from pathlib import Path

from slolidado.enums import SloProjection


@dataclass
class SloProjectionConfig:
    name: SloProjection
    epsg_code: int
    fishnet_shp: Path


class Configuration:
    SLO_LIDAR_BASE_DOWNLOAD_LINK = "http://gis.arso.gov.si/lidar"
    FISHNET_DIR = Path(__file__).parent / "fishnet"
    SLO_PROJECTION_CONFIGS = [
        SloProjectionConfig(name=SloProjection.D48GK, epsg_code=3912,
                            fishnet_shp=FISHNET_DIR / "LIDAR_FISHNET_D48.shp"),
        SloProjectionConfig(name=SloProjection.D96TM, epsg_code=3794,
                            fishnet_shp=FISHNET_DIR / "LIDAR_FISHNET_D96.shp"),
    ]

    def get_projection_config(self, projection: SloProjection):
        for projection_config in self.SLO_PROJECTION_CONFIGS:
            if projection_config.name == projection:
                return projection_config
