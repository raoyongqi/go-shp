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

	// 设置计数器，限制输出前 10 条记录
	count := 0
	maxRecords := 10

	// 遍历每一个记录
	for file.Next() {
		// 获取当前几何形状和索引
		n, p := file.Shape()

		// 打印几何形状的边界框
		fmt.Println("边界框:", p.BBox())

		// 打印属性，转换为 UTF-8 编码
		for k, f := range fields {
			val := file.ReadAttribute(n, k)
			decodedVal, err := decodeGBK(val)
			if err != nil {
				log.Printf("属性解码失败: %v", err)
				continue
			}
			fmt.Printf("\t%v: %v\n", f, decodedVal)
		}
		fmt.Println()

		// 增加计数器
		count++

		// 如果已打印了 10 条记录，退出循环
		if count >= maxRecords {
			break
		}
	}
}
