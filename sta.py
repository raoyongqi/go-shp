import geopandas as gpd
from pyproj import Transformer

# 读取Shapefile
shp_file_path = 'shp/new/filtered.shp'
gdf_projected = gpd.read_file(shp_file_path)
# 统计多边形数量
polygon_count = len(gdf_projected)

print(f"Total number of polygons: {polygon_count}")
