"""
Slovenian lidar data downloader (SloLiDaDo)
Author: Žiga Maroh
2022
"""
from pathlib import Path
from shutil import copyfileobj
from typing import Union, List
import geopandas
from slolidado import CONFIGURATION
from slolidado.enums import SloProjection, LidarDataType, SpatialJoinMethod
from requests import Session
import logging

logging.basicConfig(level=logging.INFO)


class LidarDataDownloader:
    def __init__(self, request_session: Session = Session()) -> None:
        self.request_session = request_session

    def __enter__(self) -> "LidarDataDownloader":
        return LidarDataDownloader(request_session=Session())

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.close()

    def close(self) -> None:
        self.request_session.close()
        del self

    @staticmethod
    def _get_urls_to_download(
            data_type: LidarDataType, projection: SloProjection, selected_gpd: geopandas.GeoDataFrame
    ) -> List[str]:
        if isinstance(projection, str):
            projection = SloProjection(projection)
        if isinstance(data_type, str):
            data_type = LidarDataType(data_type)

        base_url = CONFIGURATION.SLO_LIDAR_BASE_DOWNLOAD_LINK
        data_type_url_tag = data_type.get_url_tag()
        data_type_name_prefix = data_type.get_url_name_prefix(projection=projection)
        data_type_suffix = data_type.get_suffix(projection=projection)
        projection_tag = projection.value

        urls_to_download = []
        selected_gpd = selected_gpd.reset_index()
        for index, row in selected_gpd.iterrows():
            blok = row["BLOK"]
            name = row["NAME"]

            url = f"{base_url}/{data_type_url_tag}/{blok}/{projection_tag}/" \
                  f"{data_type_name_prefix}_{name}.{data_type_suffix}"
            urls_to_download.append(url)
        return urls_to_download

    def _download_files(self, urls: List[str], output_dir: Path, overwrite: bool = False) -> None:
        for url in urls:
            file_path = output_dir / url.split('/')[-1]
            if file_path.exists() and not overwrite:
                logging.info(f"File {file_path} already exist.")
                continue

            logging.info(f"Start download from URL: {url} to path: {file_path}.")
            try:
                with self.request_session.get(url, stream=True) as response:
                    if response.status_code == 200:
                        with open(file_path, 'wb') as file:
                            copyfileobj(response.raw, file)
                    else:
                        logging.error(f"Error when download from URL: {url} to path: {file_path}. Response is not 200!")
            except Exception as err:
                logging.error(f"Error when download from URL: {url} to path: {file_path}. {err}")
            logging.info(f"Finish download from URL: {url} to path: {file_path}.")

    def download(
            self,
            area_file: Union[str, Path],
            output_dir: Union[str, Path],
            projection: SloProjection = SloProjection.D96TM,
            data_type: LidarDataType = LidarDataType.DTM,
            spatial_join_method: SpatialJoinMethod = SpatialJoinMethod.INTERSECTS,
            overwrite: bool = False
    ) -> None:
        if isinstance(area_file, str):
            area_file = Path(area_file)
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        if isinstance(projection, str):
            projection = SloProjection(projection)
        if isinstance(data_type, str):
            data_type = LidarDataType(data_type)
        if isinstance(spatial_join_method, str):
            spatial_join_method = SpatialJoinMethod(spatial_join_method)

        if not area_file.is_file():
            raise ValueError("Polygon file doesn't exist!")

        if not output_dir.is_dir():
            raise ValueError("Output directory doesn't exist!")

        projection_config = CONFIGURATION.get_projection_config(projection=projection)
        if not projection_config.fishnet_shp.is_file():
            raise ValueError("Fishnet file doesn't exist!")

        try:
            fishnet_gpd = geopandas.read_file(projection_config.fishnet_shp)
        except Exception as err:
            raise Exception(f"Can't read fishnet file ({projection_config.fishnet_shp.as_posix()}). {err}")

        try:
            area_gpd = geopandas.read_file(area_file).to_crs(epsg=projection_config.epsg_code)
        except Exception as err:
            raise Exception(f"Can't read area file ({area_file.as_posix()}). {err}")

        selected_gpd = geopandas.sjoin(fishnet_gpd, area_gpd, how="inner", op=spatial_join_method.value)
        if selected_gpd.empty:
            logging.info(f"There are no tiles!")
            return None

        urls_to_download = self._get_urls_to_download(
            data_type=data_type, projection=projection, selected_gpd=selected_gpd
        )
        self._download_files(urls=urls_to_download, output_dir=output_dir, overwrite=overwrite)
        return None
