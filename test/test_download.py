from pathlib import Path
from slolidado.download import LidarDataDownloader
from slolidado.enums import SloProjection, LidarDataType, SpatialJoinMethod


def test_download():
    with LidarDataDownloader() as lidar_downloader:
        lidar_downloader.download(
            area_file=Path("data/test_area_3794.gpkg"),
            output_dir="out/",
            projection=SloProjection.D96TM,
            data_type=LidarDataType.DTM,
            spatial_join_method=SpatialJoinMethod.INTERSECTS,
            overwrite=True
        )


if __name__ == "__main__":
    test_download()
