"""
Slovenian lidar data downloader (SloLiDaDo)
Author: Žiga Maroh
2022
"""
from enum import Enum, unique


@unique
class SloProjection(Enum):
    D48GK = "D48GK"
    D96TM = "D96TM"


@unique
class LidarDataType(Enum):
    GKOT_ZLAS = "GKOT_ZLAS"
    OTR_ZLAS = "OTR_ZLAS"
    GKOT_LAZ = "GKOT_LAZ"
    OTR_LAZ = "OTR_LAZ"
    DTM = "DTM"

    def get_url_tag(self) -> str:
        if self == LidarDataType.GKOT_ZLAS:
            return "gkot"
        elif self == LidarDataType.OTR_ZLAS:
            return "otr"
        elif self == LidarDataType.GKOT_LAZ:
            return "gkot/laz"
        elif self == LidarDataType.OTR_LAZ:
            return "otr/laz"
        elif self == LidarDataType.DTM:
            return "dmr1"

    def get_url_name_prefix(self, projection: SloProjection) -> str:
        if projection == SloProjection.D96TM:
            if self == LidarDataType.GKOT_ZLAS:
                return "TM"
            elif self == LidarDataType.OTR_ZLAS:
                return "TMR"
            elif self == LidarDataType.GKOT_LAZ:
                return "TM"
            elif self == LidarDataType.OTR_LAZ:
                return "TMR"
            elif self == LidarDataType.DTM:
                return "TM1"
        elif projection == SloProjection.D48GK:
            if self == LidarDataType.GKOT_ZLAS:
                return "GK"
            elif self == LidarDataType.OTR_ZLAS:
                return "GKR"
            elif self == LidarDataType.GKOT_LAZ:
                return "GK"
            elif self == LidarDataType.OTR_LAZ:
                return "GKR"
            elif self == LidarDataType.DTM:
                return "GK1"

    def get_suffix(self, projection: SloProjection):
        if self == LidarDataType.GKOT_ZLAS:
            return "zlas"
        elif self == LidarDataType.OTR_ZLAS:
            return "zlas"
        elif self == LidarDataType.GKOT_LAZ:
            return "laz"
        elif self == LidarDataType.OTR_LAZ:
            return "laz"
        elif self == LidarDataType.DTM:
            if projection == SloProjection.D48GK:
                return "asc"
            elif projection == SloProjection.D96TM:
                return "txt"


@unique
class SpatialJoinMethod(Enum):
    INTERSECTS = "intersects"
    WITHIN = "within"
    OVERLAPS = "overlaps"
    CONTAINS = "contains"
    TOUCHES = "touches"
