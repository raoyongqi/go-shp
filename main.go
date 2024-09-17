package main

import (
	"fmt"
	"log"

	"github.com/jonas-p/go-shp"
)

func main() {
	// 打开 shapefile 文件
	file, err := shp.Open("C:/Users/r/Desktop/china/shp/vegetation_china.shp")
	if err != nil {
		log.Fatalf("打开文件时出错: %v", err)
	}
	defer file.Close()

	// 获取文件的总记录数
	fmt.Printf("总记录数: %d\n", file.AttributeCount())

	// 遍历每一个记录
}
