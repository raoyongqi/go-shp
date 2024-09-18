import matplotlib.pyplot as plt
import rasterio

# 输入 TIFF 文件路径
tif_file = 'clipped/wc2.1_5m_bio_1.tif'

# 读取裁剪后的 TIFF 文件
with rasterio.open(tif_file) as src:
    # 读取栅格数据
    data = src.read(1)  # 读取第一个波段
    
    # 获取元数据
    meta = src.meta

    # 绘制栅格数据
    plt.figure(figsize=(10, 10))
    plt.imshow(data, cmap='viridis', interpolation='none')
    plt.colorbar(label='Pixel Value')
    plt.title('Clipped TIFF Image')
    plt.xlabel('Pixel')
    plt.ylabel('Pixel')

    # 显示图像
    plt.show()
