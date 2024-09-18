import os
import glob
import xarray as xr
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
import rasterio.mask

# 输入和输出目录
input_nc_folder = 'climate/data/'
shapefile_path = 'shp/new/filtered.shp'
output_tif_folder = 'clipped/tif/'

# 确保输出目录存在
os.makedirs(output_tif_folder, exist_ok=True)

# 读取 Shapefile 数据
vector_data = gpd.read_file(shapefile_path)
vector_data = vector_data.to_crs(epsg=4326)  # 确保矢量数据在正确的投影下

# 裁剪 NetCDF 数据
def crop_nc(ds, vector_data):
    temp_raster_file = 'temp_raster.tif'
    ds.rio.to_raster(temp_raster_file, driver='GTiff', transform='auto')
    
    with rasterio.open(temp_raster_file) as src:
        out_image, out_transform = rasterio.mask.mask(src, vector_data.geometry, crop=True)
        out_meta = src.meta.copy()
        
        out_meta.update({
            'driver': 'GTiff',
            'count': out_image.shape[0],
            'height': out_image.shape[1],
            'width': out_image.shape[2],
            'transform': out_transform
        })
        
        cropped_raster_file = 'cropped_raster.tif'
        with rasterio.open(cropped_raster_file, 'w', **out_meta) as dest:
            dest.write(out_image)
    
    os.remove(temp_raster_file)
    
    cropped_ds = xr.open_rasterio(cropped_raster_file,engine='netcdf4')
    return cropped_ds

# 重采样到指定分辨率
def resample_nc_to_tif(ds, resolution, output_tif_file):
    pixel_size = resolution / 60.0  # arc-minutes to degrees
    transform, width, height = calculate_default_transform(
        ds.crs, ds.crs, ds.dims['x'], ds.dims['y'], 
        dx=pixel_size, dy=pixel_size, 
        crs=ds.crs
    )
    
    with rasterio.open(output_tif_file, 'w', driver='GTiff', 
                       height=height, width=width, 
                       count=ds.sizes['band'], dtype='float32',
                       crs=ds.crs, transform=transform) as dst:
        for i in range(ds.sizes['band']):
            reproject(
                source=xr.open_rasterio(ds)[i].values,
                destination=rasterio.band(dst, i+1),
                src_transform=ds.transform,
                src_crs=ds.crs,
                dst_transform=transform,
                dst_crs=ds.crs,
                resampling=Resampling.nearest
            )

    print(f'Resampled TIFF saved to: {output_tif_file}')

# 遍历文件夹中的所有 NetCDF 文件
nc_files = glob.glob(os.path.join(input_nc_folder, '*.nc4'))
for nc_file in nc_files:
    # 读取 NetCDF 数据
    ds = xr.open_dataset(nc_file, engine='netcdf4')
    
    for variable_name in ds.data_vars:
        print(f'Processing variable: {variable_name}')
        
        # 裁剪数据
        cropped_ds = crop_nc(ds[variable_name], vector_data)
        
        # 定义输出文件路径
        base_name = os.path.basename(nc_file).replace('.nc', f'_{variable_name}_resampled.tif')
        output_tif_file = os.path.join(output_tif_folder, base_name)
        
        # 重采样数据并保存为 TIFF
        resample_nc_to_tif(cropped_ds, resolution=5, output_tif_file=output_tif_file)
        
        # 删除裁剪后的栅格文件
        os.remove('cropped_raster.tif')

    # 关闭 NetCDF 数据集
    ds.close()

# 删除所有临时文件（如果有）
for temp_file in ['temp_raster.tif', 'cropped_raster.tif']:
    if os.path.exists(temp_file):
        os.remove(temp_file)

print("所有 NetCDF 文件已成功裁剪、重采样并保存为 TIFF 文件。")
