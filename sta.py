import dbfread
import dbf

# 定义输入输出文件路径
input_dbf = 'shp/new/filtered.dbf'
output_dbf = 'output_utf8.dbf'

# 读取 GBK 编码的 .dbf 文件
table = dbfread.DBF(input_dbf, encoding='Windows-1252')  # or 

# 输出表头信息
print(f"Field names: {table.fields}")

# 遍历并展示每条记录
for record in table.records:
    print(record.rstrip())
