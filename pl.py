import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取 GeoJSON 数据
geojson_file_path = '中华人民共和国.json'
gdf_geojson = gpd.read_file(geojson_file_path)

# 读取 Shapefile 数据
shp_file_path = 'shp/new/filtered.shp'
gdf_shp = gpd.read_file(shp_file_path)

# 定义 Albers 投影坐标系
albers_proj = ccrs.AlbersEqualArea(
    central_longitude=105,
    central_latitude=35,
    standard_parallels=(25, 47)
)

# 创建绘图对象
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': albers_proj})

# 转换 GeoJSON 数据的坐标系到自定义投影坐标系
if gdf_geojson.crs != albers_proj:
    gdf_geojson = gdf_geojson.to_crs(albers_proj)

# 转换 Shapefile 数据的坐标系到自定义投影坐标系
if gdf_shp.crs != albers_proj:
    gdf_shp = gdf_shp.to_crs(albers_proj)

# 绘制转换后的 GeoJSON 数据
gdf_geojson.plot(ax=ax, edgecolor='black', facecolor='white', alpha=0.5, label='GeoJSON Data')

# 绘制 Shapefile 数据，设置透明度
gdf_shp.plot(ax=ax, edgecolor='green', facecolor='none', linewidth=2, alpha=0.5, label='Shapefile Data')

# 添加标题
plt.title('Shapefile Data Overlay on Custom Projected GeoJSON Data')

legend_patches = [
    mpatches.Patch(color='green', label='Grassland'),
    mpatches.Patch(color='white', edgecolor='black', label='Other Areas'),
]
plt.legend(handles=legend_patches)

# 设置坐标轴标签
ax.set_xlabel('Easting (meters)')
ax.set_ylabel('Northing (meters)')

# 添加经纬度网格线
gridlines = ax.gridlines(draw_labels=True, color='gray', linestyle='--', alpha=0.5)
gridlines.xlabel_style = {'size': 10}
gridlines.ylabel_style = {'size': 10}
# 隐藏右边和上边的网格线标签
gridlines.top_labels = False
gridlines.right_labels = False
# 保存图形到文件
output_file_path = 'pic\shapefile_overlay_cartopy.png'
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')

# 显示图形
plt.show()
