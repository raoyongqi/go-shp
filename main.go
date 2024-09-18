package main

import (
	"io"
	"log"
	"strings"

	"github.com/jonas-p/go-shp"
	"golang.org/x/text/encoding/simplifiedchinese"
	"golang.org/x/text/transform"
)

func decodeGBK(s string) (string, error) {
	// Use io.ReadAll instead of ioutil.ReadAll
	reader := transform.NewReader(strings.NewReader(s), simplifiedchinese.GBK.NewDecoder())
	decoded, err := io.ReadAll(reader)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

func main() {
	// 打开 shapefile 文件
	file, err := shp.Open("C:/Users/r/Desktop/china/shp/vegetation_china.shp")
	if err != nil {
		log.Fatalf("打开文件时出错: %v", err)
	}
	defer file.Close()

	// 获取所有字段
	fields := file.Fields()

	newShpFile, err := shp.Create("shp/new/filtered.shp", shp.POLYGON) // 假设是多边形
	if err != nil {
		log.Fatal(err)
	}
	defer newShpFile.Close()

	// 创建对应的 DBF 文件，定义字段结构
	newShpFile.SetFields(fields)
	// 遍历每一个记录

	// 增加计数器
	count := 0

	for file.Next() {
		n, shape := file.Shape()

		// 假设你要处理的形状是多边形
		p := shape.(*shp.Polygon)

		for k := range fields {
			if k == 10 { // 这里是你需要的字段索引
				val := file.ReadAttribute(n, k)
				decodedVal, err := decodeGBK(val)
				if err != nil {
					log.Printf("属性解码失败: %v", err)
					continue
				}

				switch decodedVal {
				case "草甸", "草原", "草丛":
					// 将满足条件的形状写入新 shapefile
					newShpFile.Write(p)

					// 同时写入对应的属性值
					// 写入对应的属性值
					for i := range fields {
						attrValue := file.ReadAttribute(n, i)
						newShpFile.WriteAttribute(count, i, attrValue)
					}

					// fmt.Println("边界框:", p.BBox())
					// fmt.Printf("\t%v: %v\n", f, decodedVal)
					// fmt.Println()
				}
			}
		}
		count++
	}

}
