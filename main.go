package main

import (
	"fmt"
	"io"
	"log"
	"strings"

	"github.com/jonas-p/go-shp"
	"golang.org/x/text/encoding/simplifiedchinese"
	"golang.org/x/text/transform"
)

func decodeGBK(s string) (string, error) {
	// 使用 io.ReadAll 而不是 ioutil.ReadAll
	reader := transform.NewReader(strings.NewReader(s), simplifiedchinese.GBK.NewDecoder())
	decoded, err := io.ReadAll(reader)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

func main() {
	// 打开 shapefile 文件
	file, err := shp.Open("C:/Users/r/Desktop/go-shp/shp/vegetation_china.shp")
	if err != nil {
		log.Fatalf("打开文件时出错: %v", err)
	}
	defer file.Close()

	// 获取所有字段
	fields := file.Fields()
	// 输出字段名称和类型
	// 输出字段名称和类型
	for _, field := range fields {
		// Convert [11]byte to string
		gbkStr := string(field.Name[:]) // Convert to string

		// Decode field name
		decodedName, err := decodeGBK(gbkStr)
		if err != nil {
			log.Printf("Error decoding field name %s: %v", gbkStr, err)
			continue
		}
		fmt.Printf("Field Name: %s, Type:\n", decodedName)
	}
	// 创建新的 Shapefile
	newShpFile, err := shp.Create("shp/new/filtered.shp", shp.POLYGON) // 假设是多边形
	if err != nil {
		log.Fatal(err)
	}
	defer newShpFile.Close()

	// 创建对应的 DBF 文件，定义字段结构
	newShpFile.SetFields(fields)

	// 增加计数器
	count := 0

	// 遍历每一个记录
	for file.Next() {
		n, shape := file.Shape()

		// 假设你要处理的形状是多边形
		p := shape.(*shp.Polygon)

		// 获取属性字段值
		attributeMap := make(map[int]interface{})
		for k := range fields {
			val := file.ReadAttribute(n, k)
			attributeMap[k] = val // 保存所有字段的值
		}

		// 解码特定字段并判断条件
		decodedVal, err := decodeGBK(attributeMap[10].(string)) // 假设第10个字段需要解码
		if err != nil {
			log.Printf("属性解码失败: %v", err)
			continue
		}

		if decodedVal == "草甸" || decodedVal == "草原" || decodedVal == "草丛" {
			// 将满足条件的形状写入新 shapefile
			newShpFile.Write(p)

			// 同时写入对应的属性值
			for i := range fields {
				attrValue := attributeMap[i]
				newShpFile.WriteAttribute(count, i, attrValue)
			}

			// 增加计数器
			count++
		}
	}
}
