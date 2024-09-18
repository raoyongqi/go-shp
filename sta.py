import geopandas as gpd
from pyproj import Transformer

# 读取Shapefile
shp_file_path = 'shp/new/filtered.shp'
gdf_projected = gpd.read_file(shp_file_path)
# 统计多边形数量
polygon_count = len(gdf_projected)
print(f"Total number of polygons: {polygon_count}")

# 检查当前的投影坐标系
print(f"Current CRS: {gdf_projected.crs}")

# # 转换为适合面积和质心计算的投影坐标系（例如EPSG:3857）
# gdf_projected = gdf.to_crs(epsg=3857)

# 计算投影坐标系下的面积
gdf_projected['area'] = gdf_projected.geometry.area

# 计算投影坐标系下的质心
gdf_projected['centroid'] = gdf_projected.geometry.centroid

# 定义从 EPSG:3857 到 WGS84 (EPSG:4326) 的转换器
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")

# 创建新列以存储转换后的经纬度
gdf_projected['centroid_wgs84'] = gdf_projected['centroid'].apply(lambda point: transformer.transform(point.x, point.y))

# 分离出经纬度
gdf_projected['centroid_lat'] = gdf_projected['centroid_wgs84'].apply(lambda coord: coord[0])
gdf_projected['centroid_lon'] = gdf_projected['centroid_wgs84'].apply(lambda coord: coord[1])

# 按面积从大到小排序
gdf_sorted = gdf_projected.sort_values(by='area', ascending=False)

# 选择前5个多边形
top_5_gdf = gdf_sorted.head(5)

# 输出前5个多边形的面积和质心经纬度
for index, row in top_5_gdf.iterrows():
    print(f"Polygon {index}:")
    print(f"  Area: {row['area']}")
    print(f"  Centroid Longitude (WGS84): {row['centroid_lon']}")
    print(f"  Centroid Latitude (WGS84): {row['centroid_lat']}")
    print()

# 可选: 保存结果到CSV文件
# top_5_gdf[['area', 'centro
