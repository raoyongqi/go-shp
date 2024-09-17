import dbfread
import dbf

# 定义输入输出文件路径
input_dbf = 'shp/vegetation_china.dbf'
output_dbf = 'output_utf8.dbf'

# 读取 GBK 编码的 .dbf 文件
table = dbfread.DBF(input_dbf, encoding='GBK')

# 获取原 .dbf 文件的字段规格和名称
field_specs = []
field_mapping = {}  # 用于映射原字段名和新字段名
seen_fields = set()  # 用于跟踪已经添加的字段名称

for field in table.fields:
    # 截断字段名称至 8 个字符以内
    original_name = field.name[:2]  # 保证不超过 8 个字符，以防添加后缀后长度超过 10
    name = original_name
    type = field.type

    # 生成唯一的字段名称（如果出现重复，则添加后缀）
    counter = 1
    while name in seen_fields:
        name = f"{original_name[:7]}_{counter}"  # 确保总长度不超过 10
        counter += 1
    seen_fields.add(name)

    # 记录原始字段名与新字段名的映射
    field_mapping[field.name] = name

    # 根据字段类型构建规格字符串
    if type == 'C':
        field_specs.append(f"{name} C(255)")
    elif type == 'N':
        field_specs.append(f"{name} N(18, 0)")
    elif type == 'D':
        field_specs.append(f"{name} D")
    elif type == 'L':
        field_specs.append(f"{name} L")
    elif type == 'F':
        field_specs.append(f"{name} F(18, 8)")
    else:
        raise ValueError(f"Unsupported field type: {type}")

# 创建新的 UTF-8 编码的 .dbf 文件
with dbf.Table(output_dbf, field_specs=field_specs, codepage='utf8') as new_table:
    new_table.open(mode=dbf.READ_WRITE)
    
    # 将每一条记录从原表复制到新表
    for record in table:
        new_record = {field_mapping[k]: v for k, v in record.items()}
        new_table.append(new_record)

print(f"转换完成，保存为 UTF-8 编码的 .dbf 文件：{output_dbf}")