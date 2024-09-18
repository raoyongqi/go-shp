import os
import glob
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# 输入和输出目录
input_tif_folder = 'climate/tif'
output_tif_folder = 'clipped/tiff/'
shapefile_path = 'shp/new/filtered.shp'

# 读取矢量数据
vector_data = gpd.read_file(shapefile_path)

# 转换 Shapefile 的投影到 WGS84
vector_data = vector_data.to_crs(epsg=4326)

# 确保输出目录存在
os.makedirs(output_tif_folder, exist_ok=True)

# 获取所有的 TIFF 文件路径
tiff_files = glob.glob(os.path.join(input_tif_folder, '*.tif'))

for tif_file in tiff_files:
    with rasterio.open(tif_file) as src:
        # 获取栅格的投影
        raster_crs = src.crs

        # 如果栅格投影与 Shapefile 投影不一致，则需转换
        if raster_crs != vector_data.crs:
            # 重新投影矢量数据到栅格数据的投影
            vector_data = vector_data.to_crs(raster_crs)
        print(vector_data.geometry)
        # 使用矢量数据的几何裁剪栅格数据
        out_image, out_transform = mask(src, vector_data.geometry, crop=True)
        out_meta = src.meta.copy()

        # 更新元数据
        out_meta.update({
            "driver": "GTiff",
            "count": out_image.shape[0],
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # 构造输出路径
        base_name = os.path.basename(tif_file)
        output_path = os.path.join(output_tif_folder, base_name)

        # 保存裁剪后的 TIFF
        with rasterio.open(output_path, 'w', **out_meta) as dest:
            dest.write(out_image)

    print(f"裁剪完成: {tif_file} -> {output_path}")

print("所有文件已成功裁剪并保存到输出目录。")
